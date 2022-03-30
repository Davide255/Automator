import os, win32gui

from libs.LibWin import SysTrayIcon

import time

class SysTray(SysTrayIcon):

    def t_on_quit(self, *args):
        if os.environ.get('DEBUG') != None:
            win32gui.ShowWindow(os.environ['CONSOLE_HWND'], 1)
        try:
            from kivymd.app import MDApp
            MDApp().stop()
        except NameError:
            pass
        try:
            os.remove('tmp\\.runtime')
        except FileNotFoundError:
            pass
        try:
            os.remove('tmp\\UI')
        except FileNotFoundError:
            pass
        try:
            os.removedirs('tmp')
        except (FileNotFoundError, OSError):
            pass
        os._exit(0) #not use exit() or sys.exit() because it will send only a stop request that some threads ignore. 
                    #Instead use os._exit() that kills the python interpreter

    def __init__(self, icon='datab\\graphic\\logo.ico', hover_text=None, menu_options=None, on_quit=t_on_quit, on_lbutton_press=None, on_rbutton_press=None, default_menu_index=None, window_class_name=None):      
        super().__init__(icon, hover_text, menu_options=menu_options, on_quit=on_quit, on_lbutton_press=on_lbutton_press, on_rbutton_press=on_rbutton_press, default_menu_index=default_menu_index, window_class_name=window_class_name)

def change_text(*args, status:bool = True, debug: bool = False):
    from core.graphics import MainUI
    if not debug:
        if status == True:
            SysTrayIcon().EditMenuItemInfo("Open Automator UI", \
                ('Minimize', None, lambda *args: \
                    [win32gui.ShowWindow(int(os.environ['Main_Window_hWnd']), 0), change_text(status=False)]))
        else:
            SysTrayIcon().EditMenuItemInfo('Minimize', \
                ("Open Automator UI", None, lambda *args: [MainUI.eleve(), change_text(status=True)]))
    else:
        if not status:
            SysTrayIcon().EditMenuItemInfo("Hide Debug Console", \
                ("Show Debug Console", None, lambda *args: \
                    [win32gui.ShowWindow(int(os.environ['CONSOLE_HWND']), 1), change_text(status=True, debug=True)]))
            time.sleep(0.1)
        else:
            SysTrayIcon().EditMenuItemInfo("Show Debug Console", \
                ("Hide Debug Console", None, lambda *args: \
                    [win32gui.ShowWindow(int(os.environ['CONSOLE_HWND']), 0), change_text(status=False,debug=True)]))
            time.sleep(0.1)
