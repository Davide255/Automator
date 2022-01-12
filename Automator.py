'''
Automator
=========

Automator is an open source program that allow you to create automations on your system!
version: 0.13

Options
=======
-d                  to activate debug function
--console           to force the console (adding -d you can choose to hide or show the console)
--silent            to force the app to run in background without any window
--No-Sytray         to deactivate temporary the SysTray icon on the taskbar. WARNING: in this way on closing the main window the program will stop also 
                    if you have active the option "Minimize on close"!
--systemandmulti    to use the main UI also from othre programs
--V                 return the version of the main program and exit

Updates 0.13
============
- Fixed Network bug using windows API
- Adding .exe support and create first pakage
- Updated Process calsses in execute file
- Fixed general bug

Updates 0.12
============
- Added SubMenu options with new extra features.
- Hided the python console while running.
- Improved the app for a more confortable space.
- Bug fix

'''

__version__ = 0.13
__author__ = 'Davide Berardi'

import os, sys, comtypes, win32gui, win32api, win32con

if '--V' in sys.argv:
    print('Automator\nVersion:',__version__, '\nAuthor:', __author__)
    sys.exit(0)
if '-h' in sys.argv:
    print(b'\nAutomator\n\nAutomator is an open source program that allow you to create automations on your system!\nversion: 0.13\n\nOptions:\n\n-d                  to activate debug function\n--console           to force the console (adding -d you can choose to hide or show the console)\n--silent            to force the app to run in background without any window\n--No-Sytray         to deactivate temporary the SysTray icon on the taskbar. WARNING: in this way on closing the main window the program will stop also \n                    if you have active the option "Minimize on close"!\n--systemandmulti    to use the main UI also from othre programs\n--V                 return the version of the main program and exit\n'.decode('utf-8'))
    sys.exit(0)

from core.process import getallprocs

n = 0
for i in getallprocs():
    if 'Automator.exe' in i:
        n += 1
    if n > 2:
        win32gui.MessageBox(None, 'Automator is already running on your os!', 'Stratup error', win32con.MB_OK)
        sys.exit(0)

comtypes.CoUninitialize() #Un initiallize the com space for windows Runtime

import time, json, datetime
from typing import IO
win32api.SetConsoleTitle('Automator - Console')
time.sleep(0.5)
os.environ['PID'] = str(os.getpid())
console_hwnd = win32gui.FindWindow(None, 'Automator - Console')

if '--No-Systray' in sys.argv:
    os.environ['NO_SYSTRAY'] = '1'
if not '--console' in sys.argv:
    win32gui.ShowWindow(console_hwnd, 0)
    os.environ['SHOW_CONSOLE'] = '0'
else:
    os.environ['SHOW_CONSOLE'] = '1'
os.environ['CONSOLE_HWND'] = str(console_hwnd)
os.environ['PLATFORM'] = 'win32'

#Setting kivy no args
os.environ['KIVY_NO_ARGS'] = '1'
#Internal set of Automator
os.environ['NOTIFY'] = '1'

from datab.database import database
if '--first-configuration' in sys.argv:
    database().configure()
    os.environ['CONFIGURATION'] = '1'

import asyncio
if sys.version_info >= (3, 8, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from libs.LibWin import SysTrayIcon
from kivy.logger import Logger

# Block to retrive the home path of Automator
# Needed in the .exe
os.chdir(os.path.dirname(__file__))
onlyfiles = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]
if not 'Automator.exe' in onlyfiles:
    if not 'Automator.py' in onlyfiles:
        Logger.debug('Adjusting default process directory')
        from win32com.client import GetObject
        WMI = GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')                
        for p in processes :                                
            if p.Properties_("ProcessID").Value == os.getpid():
                if os.path.dirname(p.Properties_[7].Value) != os.getcwd():
                    os.chdir(os.path.dirname(p.Properties_[7].Value))
                    Logger.debug('System: File running: {}'.format(p.Properties_[7].Value))
                    Logger.debug('System: Default directory: {}'.format(os.path.dirname(p.Properties_[7].Value)))

if SysTrayIcon.is_alive():
    if os.path.isfile('tmp\\UI'):
        os.remove('tmp\\UI')
        if __name__ == '__main__':
            exit(1)
    elif os.path.isfile('tmp\\.runtime'):
        if __name__ == '__main__':
            exit(1)

if not os.path.isdir('tmp'):
    os.makedirs('tmp')

#starting a chrono for the debug
start_time = time.time()

#Base Exception 
class PythonVersionNotSupported(BaseException):
    pass
#Python Version
P_VERSION = sys.version[:3]
if not (3.6 <= float(P_VERSION) and float(P_VERSION) <= 3.9):
    raise PythonVersionNotSupported(
        'Python version {} not supported. (interpreter at {})'.format(P_VERSION, sys.executable)
        )

class UnsupportedOS(BaseException):
    pass
if sys.platform != 'win32':
    raise(UnsupportedOs('Your OS is not supported yet'))    

#essential app
if '-d' in sys.argv:
    os.environ['DEBUG'] = '1'
    Logger.setLevel('DEBUG')

#other components
from threading import Thread
from core import start

#Classe di widget già formattati
class pakedWidget():
    def switch(self, **kwargs):
        sw = MDSwitch(**kwargs)
        if kwargs.get('pos_hint') == None:
            sw.pos_hint = {'center_x': .80, 'center_y': .3}
        return sw

    def card(self, **kwargs):
        mc = MDCard(**kwargs)
        mc.orientation = 'vertical'
        mc.padding = '8dp'
        mc.size_hint = None, None
        if kwargs.get('size') == None:
            mc.size = "240dp", "280dp"
        mc.elevation = 10
        mc.border_radius = 20
        mc.radius = [15]
        return mc

    def scrollview(self, **kwargs):
        sv = ScrollView(**kwargs)
        sv.do_scroll_x = False
        sv.do_scroll_y = True
        return sv

    def gridlayout(self, **kwargs):
        gl = GridLayout(**kwargs)
        gl.size_hint_max_y = None
        if kwargs.get('cols') == None:
            gl.cols = 3
        if kwargs.get('padding') == None:
            gl.padding = "20dp"
        if kwargs.get('spacing') == None:
            gl.spacing = "20dp"
        return gl

    def boxlayout(self, **kwargs):
        bl = BoxLayout(**kwargs)
        bl.orientation = 'vertical'
        return bl

    def toolbar(self, title, **kwargs):
        tb = MDToolbar(**kwargs)
        tb.title = title
        if kwargs.get('left_action_item_bypass') != True:
            tb.left_action_items = [['menu', lambda x: UI().callback(x)]]
        return tb

#modified systrayicon class
class SysTray(SysTrayIcon):

    def t_on_quit(self, *args):
        win32gui.ShowWindow(os.environ['CONSOLE_HWND'], 1)
        try:
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
        if hover_text == None:
            hover_text = self._hover_text
        super().__init__(icon, hover_text, menu_options=menu_options, on_quit=on_quit, on_lbutton_press=on_lbutton_press, on_rbutton_press=on_rbutton_press, default_menu_index=default_menu_index, window_class_name=window_class_name)

    def run_as_thread(self):
        self._message_loop_thread = Thread(target=self._message_loop_func, daemon=True)
        self._message_loop_thread.start()
        os.environ['SysTrayIcon_Thread_Id'] = str(self._message_loop_thread.ident)

def change_text(*args, status:bool = True, debug: bool = False):
    if not debug:
        if status == True:
            SysTrayIcon().EditMenuItemInfo("Open Automator UI", ('Minimize', None, lambda *args: [UI()._hide(), change_text(status=False)]))
        else:
            SysTrayIcon().EditMenuItemInfo('Minimize', ("Open Automator UI", None, lambda *args: [UI().eleve(), change_text(status=True)]))
    else:
        if not status:
            SysTrayIcon().EditMenuItemInfo("Hide Debug Console", ("Show Debug Console", None, lambda *args: [win32gui.ShowWindow(int(os.environ['CONSOLE_HWND']), 1), change_text(status=True, debug=True)]))
            time.sleep(0.1)
        else:
            SysTrayIcon().EditMenuItemInfo("Show Debug Console", ("Hide Debug Console", None, lambda *args: [win32gui.ShowWindow(int(os.environ['CONSOLE_HWND']), 0), change_text(status=False,debug=True)]))
            time.sleep(0.1)
    
#metodo di boot              
def bootloader():
    if not __name__ == '__main__':
        return
    database().initiallize(database().load_cfg)
    if os.environ['NO_SYSTRAY'] == '1':
        Logger.warning('System: No SysTray Icon allowed, the application will leave on closing the mian UI!')
    else:
        if not '-d' in sys.argv and not '--console' in sys.argv:
            if '--silent' in sys.argv:
                settings = [("Open Automator UI", None, lambda *args: [os.remove('tmp\\UI'), change_text(status=True)])]
            else:
                settings = [('Minimize', None, lambda *args: [UI()._hide(), change_text(status=False)])]
        else:
            if os.environ['SHOW_CONSOLE'] == '0':
                settings = [("Show Debug Console", None, lambda *args: [win32gui.ShowWindow(int(os.environ['CONSOLE_HWND']), 1), change_text(status=True, debug=True)])]
            else:
                settings = [("Hide Debug Console", None, lambda *args: [win32gui.ShowWindow(int(os.environ['CONSOLE_HWND']), 0), change_text(status=False, debug=True)])]
        
            if '--silent' in sys.argv:
                settings.append(("Open Automator UI", None, lambda *args: [os.remove('tmp\\UI'), change_text(status=True)]))
            else:
                settings.append(('Minimize', None, lambda *args: [UI()._hide(), change_text(status=False)]))
        # Build SysTray menu
        menu_options = (('Audio', None, SysTrayIcon.SubMenu(#("Song metadatas", None, Audio().show_song_metas),
                            ("Play/Pause Audio", None, SysTrayIcon.Item_Deactivate),  ("Close Audio", None, SysTrayIcon.Item_Deactivate),),),
                        (None, None, SysTrayIcon.Separator),
                        *settings,
                        ('Check for Updates', None, lambda *args: os.system('Updater.exe --search-for-updates --old-v {}'.format(__version__))),
                        (None, None, SysTrayIcon.Separator),)

        SysTray("datab\\graphic\\logo.ico", "Automator", menu_options, on_lbutton_press=SysTrayIcon.show_menu).run_as_thread()
        os.environ['NO_SYSTRAY'] = '0'
        Logger.info('System: Started SysTray Icon started')
        Logger.debug('System: Started SysTray Icon started at {} with ident {}'.format(datetime.datetime.now(), os.environ['SysTrayIcon_Thread_Id']))

    if os.path.isfile('tmp\\.runtime') or os.path.isfile('tmp\\.switch_acting'):
        try:
            os.remove('tmp\\.runtime')
        except FileNotFoundError:
            pass

        try:
            os.remove('tmp\\.switch_acting')
        except FileNotFoundError:
            pass

    import kivy
    kivy.require('2.0.0')

    th = Thread(target=start.start, daemon=True)
    th.start()
    Logger.debug('System: Main threat started at {} with ident {}.'.format(datetime.datetime.now(), th.ident))
    os.environ['Main_Thread_Id'] = str(th.ident)

if __name__ == '__main__':
    bootloader()
    if '--silent' in sys.argv:
        try:
            os.makedirs('tmp')
        except FileExistsError:
            pass
        f = open('tmp\\UI', 'w')
        f.close()
        try:
            while True:
                if os.path.isfile('tmp\\UI'):
                    time.sleep(2)
                else:
                    break
        except KeyboardInterrupt:
            try:
                os.remove('tmp\\UI')
            except FileNotFoundError:
                pass

#exception that stop the application
class StopApplication(BaseException):
    pass

'''
                    IMPORT BLOCK
=====================================================
'''
from kivy.config import Config
if '--systemandmulti' in sys.argv: #add this option if you want to call automator from another python script as function
        Config.set('kivy', 'keyboard_mode', 'systemandmulti') 
Config.set('graphics', 'resizable', False)
from kivy.clock import Clock
Clock.max_iteration = 20
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.core.window import Window
#kivy screens
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
#Widgets
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDTextButton, MDFillRoundFlatButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivy.uix.widget import Widget
       
#Main class
class UI(MDApp):

    def init_temp(self, fp: IO[str]):
        runtime = {}
        for i in database().get_value('keys'):
            runtime[i] = database().get_value(i)['active']
        json.dump(runtime, fp)

    def build(self, *args):
        try:
            os.makedirs('tmp')
        except FileExistsError:
            pass

        r = open('tmp\\.runtime', 'w')
        self.init_temp(r)
        r.close()
        r = open('tmp\\.startup', 'w')
        r.close()

        self.icon = 'datab\\graphic\\logo_no_glow.ico'

        Logger.debug('GL: Attivo on_request_close e on_resize')
        Window.bind(on_request_close=self._hide)
        #Window.bind(on_minimize=lambda *args: self.on_request_close(minimize=True))

        Logger.debug('GL: creo UI.sm')
        UI.sm = ScreenManager(transition=SlideTransition())

        Logger.debug('GL: aggiungo titolo e imposto i colori')
        self.title = "Automator"
        self.theme_cls.theme_style = database().get_settings()['theme_style']
        self.theme_cls.primary_palette = "Blue"

        Logger.debug('GL: creo main screen')
        main_screen = Screen(name='main')
        main_screen.add_widget(widget=Screens.Main().build())

        Logger.debug('GL: creo settings screen')
        settings_screen = Screen(name='settings')
        settings_screen.add_widget(widget=Screens.Settings().build())

        Logger.debug('GL: creo create_screen')
        create_screen = Screen(name='create_screen')
        create_screen.add_widget(widget=Screens.Create_Screen().build())

        Logger.debug('GL: aggiungo tutti gli schermi a UI.sm')
        self.sm.add_widget(Screens.Loading_Screen().build())
        self.sm.add_widget(main_screen)
        self.sm.add_widget(settings_screen)
        self.sm.add_widget(create_screen)

        Logger.debug('GL: creo menu per main')
        self.build_menu(0, True)

        Logger.debug('GL: mostro UI')

        UI.event = Clock.schedule_once(self.stop_loading, 1)
        self.sm.current = 'loading'

        os.remove('tmp\\.startup')

        return self.sm

    def build_menu(self, *args):

        try:
            self.menu.dismiss()
        except AttributeError:
            pass

        menu_items = [
        #menu 0, main
        [
            {
                "viewclass": "OneLineListItem",
                "text": f"Apri file di Impostazioni",
                "height": dp(56),
                "on_press":lambda *args: Thread(target=database().open_conf_file, daemon=True).start(),
                "on_release": lambda *args: self.menu.dismiss(), 
            },
            {
                "viewclass": "OneLineListItem",
                "text": f"Apri file delle Automazioni",
                "height": dp(56),
                "on_press":lambda *args: Thread(target=database().open_automations_file, daemon=True).start(),
                "on_release": lambda *args: self.menu.dismiss(), 
            }
        ],
        #menu 1, settings
        [
            {
                "viewclass": "OneLineListItem",
                "text": f"Esci senza salvare",
                "height": dp(56),
                "on_release": lambda x=f"main": self.not_save(x, True),
             },
             {
                "viewclass": "OneLineListItem",
                "text": f"Salva ed esci",
                "height": dp(56),
                "on_release": lambda x=f"main": self.menu_save(x, True),
             }
        ],
        #menu 2, create_screen
        [
            {
                "viewclass": "OneLineListItem",
                "text": f"Esci senza salvare",
                "height": dp(56),
                "on_release": lambda x=f"main": self.not_save(x, True),
             },
             {
                "viewclass": "OneLineListItem",
                "text": f"Salva ed esci",
                "height": dp(56),
                "on_release": Screens.Create_Screen().confirm,
             }
        ],
        ]

        if isinstance(args[0], str):
            screens = ['main','settings','create_screen']
            itm = screens.index(args[0])
        elif isinstance(args[0], int):
            itm = args[0]
        else:
            raise TypeError(
                'Unricognizet type'
                )        

        UI.menu = MDDropdownMenu(
            items=menu_items[itm],
            width_mult=4,
        )
        if args[1] != False:
          if isinstance(args[0], str):
            self.sm.current = args[0]
          elif isinstance(args[0], int):
            screens = ['main','setting', 'create_screen']
            self.sm.current = screens[args[0]]
          else:
            raise TypeError(
                'Unricognized type'
                )
        UI.theme_style = self.theme_cls.theme_style
        UI.theme_style_bakup = self.theme_style
        self.theme_cls.theme_style = database().get_settings()['theme_style']

        '''if self.sm.current == 'settings':
            self.theme_cls.theme_style = 'Dark\''''

        Logger.info('GL: theme_style set on {}'.format(self.theme_cls.theme_style))

        return self.menu

    def build_cards(self):
        from core import Errors

        keys = database().get_value('keys')

        sv = pakedWidget().scrollview()
        cr = pakedWidget().card()
        gl = pakedWidget().gridlayout()

        if keys == None:

            lbl = MDLabel()
            lbl.text = '+'
            lbl.halign = 'center'
            lbl.font_style = 'H2'

            cr.bind(on_release=lambda *args: UI().build_menu(2, True))
            cr.add_widget(lbl)
            gl.add_widget(cr)
            sv.add_widget(gl)

            return sv
        else:
            data = database().get_data()
        
        for i in keys:
            sw = pakedWidget().switch()
            sw.id = i
            sw.bind(active=lambda sw, *args: Errors.Advises().Deactivate_Adv(sw))

            if data[i]['active']:  
                sw.active = True
            else:
                sw.active = False

            cr.add_widget(sw)    

            try:
                title = data[i]['title']
                subtitle = data[i]['subtitle']
            except KeyError:
                print('card must have title and a subtitle')
                exit(0)

            for v in data[i]['added_propriety']:
                try:
                    if v == 'text_color':
                        text_color = data[i][v]
                    elif v == 'text_style':
                        text_style = data[i][v]
                    elif v == 'bg_color':
                        bg_color = data[i][v]
                    else:
                        pass
                except KeyError or AttributeError:
                    pass

            lbl = MDLabel(text=title, font_style='H5')
            lbl.halign = 'center'
            lbl.valign = 'top'
            cr.add_widget(lbl)
            cr.ids['title'] = lbl.text

            lbl = MDLabel(text=subtitle, text_size='10dp')
            lbl.halign = 'center'
            lbl.valign = 'center'
            cr.add_widget(lbl)
            cr.ids['subtitle'] = lbl.text

            cr.bind(on_release=lambda *args: Screens.Template_automation_screen().dispatch(args[0]))
            gl.add_widget(cr)
            cr = pakedWidget().card() #empty the variable

        lbl = MDLabel()
        lbl.text = '+'
        lbl.halign = 'center'
        lbl.font_style = 'H2'

        cr.bind(on_release=lambda *args: UI().build_menu(2, True))
        cr.add_widget(lbl)
        gl.add_widget(cr)
        sv.add_widget(gl)

        return sv

    def stop_loading(self, *args):
        UI.sm.current= 'main'
        hWnd = 0
        while True:
            hWnd = win32gui.FindWindow(None, self.title)
            try:
                assert hWnd
                os.environ['Main_Window_hWnd'] = str(hWnd)
                break
            except AssertionError:
                pass
        database().manage_winreg()
    
    def active_switch(self, *args):
        try:
            if self.theme_style == 'Dark':
                return True
            else:
                return False
        except AttributeError:
            self.theme_style = self.theme_cls.theme_style
            
            if self.theme_style == 'Dark':
                return True
            else:
                return False
            
    def change_theme_cls_theme_style(self, *args):
        
        if self.theme_style == 'Light':
            self.theme_style = 'Dark'
            snack_text = 'tema scuro attivato'
        else:
            self.theme_style = 'Light'
            snack_text = 'tema scuro disattivato'

        self.send_snackbar(text=snack_text)

    def send_snackbar(self, **kwargs):
        self.snackbar = Snackbar(
        text=kwargs.get('text'),
        snackbar_x="10dp",
        snackbar_y="10dp",
        )
        self.snackbar.size_hint_x = (
            Window.width - (self.snackbar.snackbar_x * 2)
        ) / Window.width

        try:
            self.snackbar.buttons = kwargs.get('buttons')
            '''[
            MDFlatButton(
                text="UPDATE",
                text_color=(1, 1, 1, 1),
                on_release=snackbar.dismiss,
            ),
            MDFlatButton(
                text="CANCEL",
                text_color=(1, 1, 1, 1),
                on_release=snackbar.dismiss,
            ),
            ]'''
        except ValueError:
            self.snackbar.buttons = []

        try:
            self.snackbar.dismiss()
            self.snackbar.open()
        except AttributeError:
            self.snackbar.open()

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_save(self, *args):
        database().set('theme_style', self.theme_style)
        self.theme_cls.theme_style = self.theme_style
        self.build_menu(*args)

    def not_save(self, *args):
        self.theme_cls.theme_style = self.theme_style_bakup
        self.build_menu(*args)

    def eleve(self, *args):
        #using Windows API to raise the window for a major speed
        win32gui.ShowWindow(int(os.environ['Main_Window_hWnd']), 1)
    
    def _hide(self, *args):
        #using Windows API to hide the window for a major speed
        if (database().get_settings()['hide_on_close'] and os.environ['NO_SYSTRAY'] != '1'):
            state = 0
            if os.environ['NOTIFY'] == '1':
                database().send_notification('Automator', 'Automator è ancora in esecuzione in background!')
                os.environ['NOTIFY'] = '0'
        elif (not database().get_settings()['hide_on_close'] or os.environ['NO_SYSTRAY'] == '1'):
            win32gui.MessageBeep(win32con.IDI_INFORMATION)
            res = win32gui.MessageBox(os.environ.get('Main_Window_hWnd'), 'If exit, Automations will not start!','LEAVE?', win32con.MB_OKCANCEL | win32con.MB_ICONINFORMATION) 
            if res == win32con.IDOK:
                Window.close()
                Logger.debug('System: Process ended in {}'.format(datetime.datetime.fromtimestamp(time.time() - start_time).strftime("%M:%S")))
                raise StopApplication()
            else:
                return True
        else:
            state = 2
        if state == 0:
            SysTrayIcon().EditMenuItemInfo('Minimize', ("Open Automator UI", None, lambda *args: [UI().eleve(), change_text(status=True)]))
        win32gui.ShowWindow(int(os.environ['Main_Window_hWnd']), state)
        return True     

#Classe di schermi
class Screens:

    class Loading_Screen(Screen):
        
        def build(self):
            ls = Screen(name='loading')
            from kivymd.uix.spinner import MDSpinner
            from kivy.metrics import dp
            box = FloatLayout()
            lbl = MDLabel(text='Caricamento...', halign='center')
            lbl.pos_hint = {'center_x':.5, 'center_y':.55}
            box.add_widget(lbl)
            box.add_widget(MDSpinner(
                                size_hint=(None, None),
                                size=(dp(46), dp(46)),
                                pos_hint={'center_x': .5, 'center_y': .45},
                                active=True,
                                palette=[
                                    [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],
                                    [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],
                                    [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],
                                    [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
                                ]
                            ))
            ls.add_widget(box)
            return ls

    class Main(Screen):

        def build(self):
            bx = pakedWidget().boxlayout()
            bx.add_widget(pakedWidget().toolbar('Automator'))
            sv = UI.build_cards(UI)
            bx.add_widget(sv)

            return bx        

    class Settings(Screen):
        
        def build(self):
            bx = pakedWidget().boxlayout()
            bx.add_widget(pakedWidget().toolbar('Impostazioni'))

            sv = pakedWidget().scrollview()
            #gl = GridLayout(row_force_default=True, cols = 4, padding = [30,30,30,30], row_default_height =  100)
            fl = FloatLayout()

            '''lbl = MDLabel(text='tema scuro')
            gl.add_widget(lbl)
            switch = MDSwitch()
            switch.active = UI().active_switch()
            switch.bind(active=UI().change_theme_cls_theme_style)
            gl.add_widget(switch)'''

            lbl = MDLabel(text='language', pos_hint={'center_x':.2, 'center_y':.2})
            fl.add_widget(lbl)
            drop = DropDown()
            ita = MDRaisedButton(text='ita', on_press=lambda *args: print('pressed ita'))
            drop.add_widget(ita)
            engl = MDRaisedButton(text='engl', on_press=lambda *args: print('pressed engl'))
            drop.add_widget(engl)
            main_button = MDTextButton(text='chose', pos=(50, 50))
            main_button.bind(on_release=drop.open)
            fl.add_widget(main_button)

            #sv.add_widget(fl)
            bx.add_widget(fl)

            return bx

    class Create_Screen():
        widgetref = {}
        
        def build(self):
            bx = pakedWidget().boxlayout()
            tb = pakedWidget().toolbar('Create New Automation')
            bx.add_widget(tb)
            sv = pakedWidget().scrollview()
            fl = FloatLayout()
            self.widgetref['float_layout'] = fl
            gl = pakedWidget().gridlayout(cols=2)

            self.TitleBox = MDTextField(hint_text='Titolo', required=True, mode='fill', helper_text_mode='on_error', helper_text= "Il campo è obbligatorio")
            self.DescriptionBox = MDTextField(mode='fill', hint_text= "Descrizione (opzionale)")
            #adding a ref
            self.widgetref['title'] = self.TitleBox
            self.widgetref['subtitle'] = self.DescriptionBox
            #adding the widgets at the grid layout
            gl.add_widget(self.TitleBox)
            gl.add_widget(self.DescriptionBox)
            #creating automation chooser
            lbl = MDLabel(text='Agenti', pos_hint={'center_x':.5,'center_y':.78}, halign='center', font_style='H6')
            fl.add_widget(lbl)
            icb = MDIconButton(icon='datab\\graphic\\+.png', pos_hint={'center_x':.5,'center_y':.66}, on_release=lambda *args: self.agent_button_callback(*args))
            self.widgetref['agent_+_button'] = icb
            fl.add_widget(icb)
            lbl= MDLabel(text='Azioni', pos_hint={'center_x':.5,'center_y':.54}, halign='center', font_style='H6')
            self.widgetref['actions_to_do_lbl'] = lbl
            fl.add_widget(lbl)
            icb = MDIconButton(icon='datab\\graphic\\+.png', pos_hint={'center_x':.5,'center_y':.42}, on_release=lambda *args: self.actions_to_do_button_callback(*args))
            self.widgetref['actions_to_do_+_button'] = icb
            fl.add_widget(icb)
            #cr = pakedWidget().card(size=("700dp","60dp"), pos_hint={'center_x':.5,'center_y':.40})
            #fl.add_widget(cr)
            fl.add_widget(gl)
            sv.add_widget(fl)
            bx.add_widget(sv)

            return bx

        def select_from_dialog(self, dialog_histance=None, dialog_type=1):
            cls = BoxLayout(size_hint_y = None)
            lbl = MDLabel(text='Aggiungi un\'Agente che attiverà la tua automazione.', pos_hint={'center_x':.5, 'center_y':.9})
            cls.add_widget(lbl)
            icb = MDIconButton(icon='datab\\graphic\\+.png')#, pos_hint={'center_x':.1, 'center_y':.3})
            cls.add_widget(icb)

            if dialog_histance != None:
                return dialog_histance.dismiss()

            self.dialog = MDDialog(
                title='Create new',
                text='Choose an agent that will start your automation',
                size_hint= [0.5, None],
                size_hint_y = .8,
                type='custom',
                content_cls=cls,
                buttons = [
                    MDFlatButton(

                    ),
                    MDFillRoundFlatButton(
                                text='OK'),
                ]
            )
            self.dialog.bind(on_dismiss= lambda *args: self.modify_ui())

            return self.dialog

        def modify_ui(self, *args, **kwargs):
            #addig the icons at a list
            card_widget = []
            xicon = MDIconButton(icon='datab\\graphic\\x-icon.png', pos_hint={'center_x':.9, 'center_y':5}, user_font_size='9dp')
            card_widget.append(xicon)
            editicon = MDIconButton(icon='datab\\graphic\\edit-icon.png', pos_hint={'center_x':.82, 'center_y':.5}, user_font_size='9dp')
            card_widget.append(editicon)
            #declaring fl
            fl = self.widgetref['float_layout']
            #checking if rem_widget is a string or a Widget
            if kwargs.get('rem_widget') != None:
                if isinstance(kwargs.get('rem_widget'), str):
                    fl.remove_widget(self.widgetref[kwargs.get('rem_widget')])
                else:
                    fl.remove_widget(kwargs.get('rem_widget'))
            try:
                if self.widgetref['agent_card'] == False:
                    cr = pakedWidget().card(size=("700dp","80dp"), pos_hint={'center_x':.5,'center_y':.66})
                else:
                    Clock.unschedule(self.modify_ui)
                    return None
            except KeyError:
                cr = pakedWidget().card(size=("700dp","80dp"), pos_hint={'center_x':.5,'center_y':.66})
            #adding all the icons in the MDCard
            for i in card_widget:
                cr.add_widget(i)
            fl.add_widget(cr)
            self.widgetref['agent_card'] = True
            Clock.unschedule(self.modify_ui)
            return None

        def agent_button_callback(self, *args):
            print('aggiungo')
            os.environ['DIALOG_STATUS'] = 'open'
            self.select_from_dialog().open()

        def actions_to_do_button_callback(self, *args):
            #print('prova',*args)
            #Clock.schedule_interval(self.modify_ui, 0.2)
            pass

        def confirm(self, *args):
            import uuid
            
            data = {'card {}'.format(uuid.uuid4()):
                    {'title':self.widgetref['title'].text,
                    'subtitle': self.widgetref['subtitle'].text,
                    'active': True,
                    "actions": {
                        "automation": [],
                        "action_to_do": []
                        }
                    }
                   }

            print(data)
            #print(database().get_data())

            UI().build_menu('main', True)

    class Template_automation_screen:

        def dispatch(self, widget=None):
            if widget == None:
                screen = self._empty()
            elif isinstance(widget, Widget):
                title = widget.ids['title']
                for i in database.data:
                    if i['title'] == title:
                        self.data = i
                        break
                self.title = title
                self.id = database.data.index(self.data)
                self.subtitle = self.data['subtitle']
                self.active = self.data['active']
                self.actions = self.data['actions']
                screen = self._build()

            if not UI.sm.has_screen(screen.name):
                UI.sm.add_widget(screen)
            else:
                widgets = screen.children.copy()
                scr = UI.sm.get_screen(self.title)
                scr.clean_widgets()
                scr.add_widget(widgets)
            UI.sm.current = self.title
            return None  
            
        def _empty(self):
            pass

        def _build_widget(self):
            pass

        def _build(self):
            scr = Screen(name=self.title)
            bx = pakedWidget().boxlayout()
            tb = pakedWidget().toolbar(self.title)
            bx.add_widget(tb)
            gl = pakedWidget().gridlayout(cols=2)
            gl.add_widget(MDLabel(text=self.title, font_style='H2'))
            gl.add_widget(MDLabel(text=self.title, font_style='H2'))
            bx.add_widget(gl)
            scr.add_widget(bx)
            return scr

#Entry point
if __name__ == '__main__':
    try:
        UI().run()
        try:
            is_t_alive = True
            while is_t_alive != False:
                time.sleep(15)
        except StopApplication:
            Logger.debug('System: Process ended in {}'.format(datetime.datetime.fromtimestamp(time.time() - start_time).strftime("%M:%S")))
            sys.exit(1)

    except (KeyboardInterrupt, StopApplication):
        win32gui.ShowWindow(os.environ['CONSOLE_HWND'], 1)
        Logger.warning('Interrupt detected, abort')
        try:
            os.remove(os.path.join(os.path.dirname(__file__), 'tmp', '.runtime'))
        except FileNotFoundError:
            pass

        try:
            os.removedirs(os.path.join(os.getcwd(), 'tmp'))
        except (FileNotFoundError, OSError):
            pass
        
        Logger.debug('System: Process ended in {}'.format(datetime.datetime.fromtimestamp(time.time() - start_time).strftime("%M:%S")))

    except ChildProcessError as e:
        Logger.warning(e)
 