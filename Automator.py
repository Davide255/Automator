'''
Automator
=========

Automator is an open source program that allow you to create automations on your system!
version: 0.13
compatibility: Python 3.6 <> 3.9

Options
=======
-d                      to activate debug function
--set-logger-level [level]
                        to set costum level, levels are ['DEBUG', 'INFO', 'WARNING', 'ERROR']
--disable-logger        to disable the logger function, THIS WILL DISPLAY NOATHING ON THE CONSOLE
--console               to force the console (adding -d or setting DEBUG logger you can choose to hide or show the console)
--silent                to force the app to run in background without any window
--no-systray            to deactivate temporary the SysTray icon on the taskbar. WARNING: in this way on closing the main window 
                        the program will stop also if you have active the option "Minimize on close"!
--V -V                  return the version of the main program and exit
-h --help               show an help message and exit
--help-console          show the help message on the console

Updates 0.14
============
- Adding First-Startup configuration
- 
- Bug Fixed

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

import sys

class UnsupportedOS(BaseException):
    pass

if sys.platform != 'win32': # Automator works only on windows yet
    raise UnsupportedOS('Your OS is not supported yet')

try:
    import os, win32gui, win32con, time
except ImportError:
    import os, sys
    if not input('Some modules are missing!\nWould you install them now? [y/n] ') == 'n':
        from Install_Helpers import Installation_Helper
        Installation_Helper(ffmpeg=False, libav=False).install()
    path = sys.argv[0]
    print('\n<----------------- Restarting ----------------->\n')
    os.system('{} {} {} --force-logging'.format(sys.executable, path, sys.argv[0:]))
    sys.exit(0)

if '--listdir' in sys.argv:
    print(os.listdir(os.path.dirname(__file__)))
    sys.exit(0)

#starting a chrono for the debug
start_time = time.time()  

from datab import env_vars

env_vars.START_TIME = start_time

argv = sys.argv.copy() #copy the command-line args in a variable

if '--V' in sys.argv or '-V' in sys.argv:
    print('Automator\nVersion:',__version__, '\nAuthor:', __author__)
    sys.exit(0)
if '-h' in sys.argv or '--help' in sys.argv:
    if '-h' in sys.argv:
        argv.remove('-h')
    else:
        argv.remove('--help')
    from datab.env_vars import HELP_MESSAGE
    win32gui.MessageBox(None, HELP_MESSAGE, 'Automator', win32con.MB_OK)
    sys.exit(0)

if '--help-console' in sys.argv:
    argv.remove('--help-console')
    from datab.env_vars import HELP_CONSOLE
    print(HELP_CONSOLE)
    sys.exit(0)

if '--modify-install' in sys.argv:
    if '--check' in sys.argv:
        from Install_Helpers import Installation_Helper
        Installation_Helper().install()
        sys.exit(0)

#Base Exception 
class PythonVersionNotSupported(BaseException):
    pass
P_VERSION = sys.version[:3] #Python Version as float
if not (3.6 <= float(P_VERSION) and float(P_VERSION) <= 3.9):
    raise PythonVersionNotSupported(
        'Python version {} not supported. (interpreter: {})'.format(P_VERSION, sys.executable)
        )

if '--disable-logger' in sys.argv:
    os.environ['KIVY_NO_CONSOLELOG'] = '1'
    argv.remove('--disable-logger')
#Setting kivy no args
os.environ['KIVY_NO_ARGS'] = '1'

from datab.database import database

from core.process import getallprocs
try:
    import comtypes
except (ModuleNotFoundError, ImportError):
    if not input('Some modules are missing!\nWould you install them now? [y/n] ') == 'n':
        from Install_Helpers import Installation_Helper
        Installation_Helper(ffmpeg=False, libav=False).install()
    path = sys.argv[0]
    print('\n<----------------- Restarting ----------------->\n')
    os.system('{} {} {}'.format(sys.executable, path, sys.argv[0:]))
    sys.exit(0)
import datetime, win32api
win32api.SetConsoleTitle('Automator - Console')
time.sleep(0.5)
os.environ['PID'] = str(os.getpid())
console_hwnd = win32gui.FindWindow(None, 'Automator - Console')

#Settings
os.environ['NOTIFY'] = '1'
if '--no-systray' in sys.argv:
    argv.remove('--no-systray')
    os.environ['NO_SYSTRAY'] = '1'
if not '--console' in sys.argv:
    win32gui.ShowWindow(console_hwnd, 0)
    os.environ['SHOW_CONSOLE'] = '0'
else:
    argv.remove('--console')
    os.environ['SHOW_CONSOLE'] = '1'
try:
    assert console_hwnd
except AssertionError:
    console_hwnd = 0
os.environ['CONSOLE_HWND'] = str(console_hwnd)
os.environ['PLATFORM'] = 'win32'
os.environ['NO_MEDIA_PLAYER_WINRT_MESSAGE'] = '1'

#kivy datas
os.environ['KIVY_IMAGE'] = "pil,sdl2"
os.environ['PATH'] += ';' + os.path.expandvars('%AppData%\\Python\\share\\glew\\bin')
os.environ['PATH'] += ';' + os.path.expandvars('%AppData%\\Python\\share\\sdl2\\bin')

if '--force-logging' in sys.argv:
    print('feature under development')
    import logging
    logging.basicConfig(level='DEBUG')
    os.environ['KIVY_NO_CONSOLELOG'] = '1' #suppress kivy logger
    argv.remove('--force-logging')

try:
    from kivy.logger import Logger
except (ModuleNotFoundError, ImportError):
    if not input('Some modules are missing!\nWould you install them now? [y/n] ') == 'n':
        from Install_Helpers import Installation_Helper
        Installation_Helper(ffmpeg=False, libav=False).install()
    path = sys.argv[0]
    print('\n<----------------- Restarting ----------------->\n')
    os.system('{} {} {}'.format(sys.executable, path, sys.argv[0:]))
    sys.exit(0)

if '--set-logger-level' in sys.argv:
    if '--force-logging' in sys.argv:
        level = sys.argv[sys.argv.index('--set-logger-level')+1]
        if level in ['DEBUG', 'INFO', 'WARNING', 'CRITICAL', 'ERROR']:
            logging.basicConfig(level=level)
    else:
        level = sys.argv[sys.argv.index('--set-logger-level')+1]
        if level in ['DEBUG', 'INFO', 'WARNING', 'CRITICAL', 'ERROR']:
            Logger.setLevel(level)
        else:
            Logger.warning('System: level: {} not recognized, levels are DEBUG, INFO, WARNING, CRITICAL, ERROR'.format(level))
    argv.remove(level)
    argv.remove('--set-logger-level')

# Retrive the home path of Automator
# Needed in the .exe
os.chdir(os.path.dirname(os.path.realpath(__file__)))
onlyfiles = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]
if not 'Automator.exe' in onlyfiles:
    if not 'Automator.py' in onlyfiles:
        os.environ['BINARY_MODE'] = '1'
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

if '--ignore-bin' in sys.argv:
    os.environ.pop('BINARY_MODE')
    argv.remove('--ignore-bin')

n = 0
for i in getallprocs():
    if 'Automator.exe' in i:
        n += 1
    if n > 2: #If Automator is running, it rises his window!
        Logger.warning('System: Automator is already running!')
        if os.path.isfile('tmp\\UI'): #If is in silent mode, it wakes it up
            os.remove('tmp\\UI')
        else: #Else, find his window and blink it!
            hwnd = win32gui.FindWindow(None, 'Automator')
            win32gui.ShowWindow(hwnd, 1)
            win32gui.FlashWindow(hwnd, True)
        sys.exit(0)

comtypes.CoUninitialize() #Uninitiallize the com space for windows Runtime

#Setting kivy no args
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_IMAGE'] = "pil,sdl2"
os.environ['PATH'] += ';' + os.path.expandvars('%AppData%\\Python\\share\\glew\\bin')
os.environ['PATH'] += ';' + os.path.expandvars('%AppData%\\Python\\share\\sdl2\\bin')
#Internal set of Automator
os.environ['NOTIFY'] = '1'

if '--first-configuration' in sys.argv:
    argv.remove('--first-configuration')
    if not os.path.isdir('dlls'):
        win32gui.MessageBeep(win32con.MB_ICONERROR)
        res = win32gui.MessageBox(None, 
        'La directory "{}" non è stata trovata, provare a reinstallare il programma o scricare i files interessati da GitHub.',
        'CRITICAL ERROR, DLLS MISSING', win32con.MB_OK | win32con.MB_ICONERROR)
        if res:
            pass
        exit(0)
    os.environ['FIRST_SETUP'] = '1'
    import webbrowser
    webbrowser.open('https://github.com/Davide255/Automator/blob/2f82620ffcf594604ead1f74c0f8952db1e193f5/README.md')

if '-d' in sys.argv: #Debug mode
    if os.environ.get('KIVY_NO_CONSOLELOG'):
        print('Logger disattivato, opzione -d ignorata')
    else:
        os.environ['DEBUG'] = '1'
        Logger.setLevel('DEBUG')
        argv.remove('-d')

if '--force-dark-theme' in sys.argv and database().get_settings()['theme_style'] == 'Dark':
    os.environ['FORCE_DARK'] = '1'
    argv.remove('--force-dark-theme')
elif '--force-dark-theme' in sys.argv:
    if __name__ == '__main__':
        print('=========')
        Logger.warning('Theme: \'--force-dark-theme\' works only if theme is set to Dark (current: {})'.format(database().get_settings()['theme_style']))
        print('=========')
    argv.remove('--force-dark-theme')

if '--silent' in argv:
    argv.remove('--silent') #this will be processed after
if '--no-execute' in argv:
    argv.remove('--no-execute')
if len(argv) > 1:
    if __name__ == '__main__':
        Logger.warning('INPUT: Skipped arguments: {}'.format(', '.join(argv[1:])))

import asyncio
if sys.version_info >= (3, 8, 0): #If python version is > than 3.8.0 asyncio must set his policy to WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from libs.LibWin import SysTrayIcon

if not os.path.isdir('tmp'):
    os.makedirs('tmp')

from threading import Thread
from core import start

from core import SysTray, change_text
from core.graphics import MainUI

def bootloader(): #metodo di boot 
    if not __name__ == '__main__': #don't restart if called from other threads
        return
    database().initiallize(database().load_cfg)
    if os.environ['NO_SYSTRAY'] == '1':
        Logger.warning('System: No SysTray Icon allowed, the application will leave on closing the mian UI!')
    else:
        if not os.environ.get('DEBUG') and int(os.environ.get('SHOW_CONSOLE')):
            if '--silent' in sys.argv:
                settings = [("Open Automator UI", None, lambda *args: [os.remove('tmp\\UI'), change_text(status=True)])]
            else:
                settings = [('Minimize', None, lambda *args: \
                    [win32gui.ShowWindow(int(os.environ['Main_Window_hWnd']), 0), change_text(status=False)])]
        else:
            if int(os.environ['CONSOLE_HWND']) == 0:
                settings = [("Hide Debug Console", None, SysTrayIcon.Item_Deactivate)]
            else:
                if os.environ['SHOW_CONSOLE'] == '0':
                    settings = [("Show Debug Console", None, lambda *args: [win32gui.ShowWindow(int(os.environ['CONSOLE_HWND']), 1), change_text(status=True, debug=True)])]
                else:
                    settings = [("Hide Debug Console", None, lambda *args: [win32gui.ShowWindow(int(os.environ['CONSOLE_HWND']), 0), change_text(status=False, debug=True)])]
        
            if '--silent' in sys.argv:
                settings.append(("Open Automator UI", None, lambda *args: [os.remove('tmp\\UI'), change_text(status=True)]))
            else:
                settings.append(('Minimize', None, lambda *args: \
                    [win32gui.ShowWindow(int(os.environ['Main_Window_hWnd']), 0), change_text(status=False)]))
        # Build SysTray menu
        menu_options = (('Audio', None, SysTrayIcon.SubMenu(#("Song metadatas", None, Audio().show_song_metas),
                            ("Play/Pause Audio", None, SysTrayIcon.Item_Deactivate),  ("Close Audio", None, SysTrayIcon.Item_Deactivate),),),
                        (None, None, SysTrayIcon.Separator),
                        *settings,
                        ('Check for Updates', None, lambda *args: Thread(target=os.system, args=('Updater.exe --search-for-updates --old-v {}'.format(database.settings['program_settings']['version']),)).start()),
                        (None, None, SysTrayIcon.Separator),)

        SysTray("datab\\graphic\\logo.ico", "Automator", menu_options, on_lbutton_press=SysTrayIcon.show_menu).start(daemon=True)
        os.environ['NO_SYSTRAY'] = '0'
        Logger.info('System: Started SysTray Icon started')
        Logger.debug('System: Started SysTray Icon started at {}'.format(datetime.datetime.now()))

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

    if not '--no-execute' in sys.argv:
        th = Thread(target=start.start, daemon=True)
        th.start()
        Logger.debug('System: Main thread started at {} with ident {}.'.format(datetime.datetime.now(), th.ident))
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

from core.exceptions import StopApplication

'''
               GRAPHICS IMPORT BLOCK
=====================================================
'''
from kivy.config import Config
if '--systemandmulti' in sys.argv: #add this option if you want to call automator from another python script as function
    Config.set('kivy', 'keyboard_mode', 'systemandmulti') 
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivy.clock import Clock
Clock.max_iteration = 20

from core.graphics.MainUI import UI

#Entry point
if __name__ == '__main__':
    try:
        UI().run()

    except KeyboardInterrupt:
        Logger.warning('KeyboardInterrupt detected, abort')
        win32gui.ShowWindow(os.environ['CONSOLE_HWND'], 1)
        from core.audio.Audio import Audio
        Audio().quit()
        try:
            os.remove(os.path.join(os.path.dirname(__file__), 'tmp', '.runtime'))
        except FileNotFoundError:
            pass

        try:
            os.removedirs(os.path.join(os.getcwd(), 'tmp'))
        except (FileNotFoundError, OSError):
            pass
        
        Logger.debug('System: Process ended in {}'.format(datetime.datetime.fromtimestamp(time.time() - start_time).strftime("%M:%S")))

    except StopApplication:
        win32gui.ShowWindow(os.environ['CONSOLE_HWND'], 1)
        from core.audio.Audio import Audio
        Audio().quit()
        try:
            os.remove(os.path.join(os.path.dirname(__file__), 'tmp', '.runtime'))
        except FileNotFoundError:
            pass

        try:
            os.removedirs(os.path.join(os.getcwd(), 'tmp'))
        except (FileNotFoundError, OSError):
            pass
        
        Logger.debug('System: Process ended in {}'.format(datetime.datetime.fromtimestamp(time.time() - start_time).strftime("%M:%S")))
