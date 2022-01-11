from __future__ import absolute_import, print_function, unicode_literals

from datab.env_vars import ICON, KIVY_LOGO, SET_REG_KEY_CODE, SETTINGS

# standard library
try:
    import os, json
    import logging as Logger
    from datab.env_vars import DATABASE
    from libs.LibWin import Notifier
except ImportError:
    None

class database():
    keys = {}
    returnv = False
    pause = False
    dynamic_key_stop = False
    PATH = 'datab\\Automator.json'
    bools = {'true':True, 'false':False}
    
    def initiallize(self, *On_succes_functions):
        if not os.path.isfile('datab\\.config'):
            if not os.path.isdir('datab'):
                os.makedirs('datab')
            f = open('datab\\.config', 'w')
            f.write(SETTINGS)
            f.close()

        os.environ['close'] = '0'
        if not os.path.isfile(self.PATH):
            if not os.path.isdir('datab'):
                os.makedirs('datab')
            with open(database.PATH, 'w', encoding='utf-8') as f:
                f.write(DATABASE)
                f.close()
        
        if not os.path.isfile('datab\\graphic\\logo.ico'):
            if not os.path.isdir('datab\\graphic'):
                os.makedirs('datab\\graphic')
            f = open('datab\\graphic\\logo.ico', 'wb')
            f.write(ICON)
            f.close()
            f = open('datab\\graphic\\Kivy_logo.ico', 'wb')
            f.write(KIVY_LOGO)
            f.close()

        try:
            os.environ['PLATFORM']
        except KeyError:
            raise ChildProcessError('Variabile PLATFORM not found')

        database.PLATFORM = os.environ['PLATFORM']
        try:
            database.PATH
        except AttributeError:
            database.PATH = 'datab\\Automator.json'

        if os.path.isfile(self.PATH):
            with open(self.PATH) as f:
                js = json.load(f)
                database.data = js
            f.close()
        else:
            pass
        Logger.debug('System: Database class initialized succesfully!')
        for i in On_succes_functions:
            if callable(i):
                i(self)
            else:
                pass
        return
    
    def open_conf_file(self, *args):
        os.system('START /wait notepad datab\.config')
        database.settings = dict()
        database().initiallize(database().get_settings, database().load_cfg)
        import win32gui, win32con
        win32gui.MessageBox(os.environ.get('Main_Window_hWnd'), 'Some settings requires a reboot to ba applyed.','INFO', win32con.MB_OK | win32con.MB_ICONINFORMATION) 
    
    def open_automations_file(self, *args):
        os.system('START /wait notepad datab\Automator.json')
        import win32gui, win32con
        win32gui.MessageBox(os.environ.get('Main_Window_hWnd'), 'Automations requires a reboot to ba loaded and executed.','INFO', win32con.MB_OK | win32con.MB_ICONINFORMATION) 

    def manage_winreg(self, cfg=None):
        if not cfg:
            import configparser
            cfg = configparser.ConfigParser()
            cfg.read('datab\\.config')

        '''try:
            hwnd = ' --hwnd ' + os.environ['Main_Window_hWnd']
        except KeyError:'''
        hwnd = ''
        if database().get_settings()['start_with_windows'] and not cfg.getboolean('program_settings', 'is_winreg_key'):
            if not os.path.isfile(os.path.join(os.getcwd(), 'tmp', 'set_reg_key.py')):
                f = open(os.path.join(os.getcwd(), 'tmp', 'set_reg_key.py'), 'w')
                f.write(SET_REG_KEY_CODE)
                f.close()
            os.system('START /wait /min ' + os.path.join(os.getcwd(), 'tmp', 'set_reg_key.py') + ' --add-winreg ' + os.path.join(os.getcwd(), 'Automator.exe') +' --silent' + hwnd)
            if os.path.isfile('tmp\\.SUCCESS'):
                cfg.set('program_settings', 'is_winreg_key', 'true')
                with open('datab\\.config', 'w') as configfile:
                    cfg.write(configfile)
                os.remove('tmp\\.SUCCESS')
        elif not database().get_settings()['start_with_windows'] and cfg.getboolean('program_settings', 'is_winreg_key'):
            if not os.path.isfile(os.path.join(os.getcwd(), 'tmp', 'set_reg_key.py')):
                f = open(os.path.join(os.getcwd(), 'tmp', 'set_reg_key.py'), 'w')
                f.write(SET_REG_KEY_CODE)
                f.close()
            os.system('START /wait /min ' + os.path.join(os.getcwd(), 'tmp', 'set_reg_key.py') + ' --remove-winreg' + hwnd)
            if os.path.isfile('tmp\\.SUCCESS'):
                cfg.set('program_settings', 'is_winreg_key', 'false')
                with open('datab\\.config', 'w') as configfile:
                    cfg.write(configfile)
                os.remove('tmp\\.SUCCESS')
        if os.path.isfile('tmp\\set_reg_key.py'):
            os.remove('tmp\\set_reg_key.py')

    def send_notification(self, title, msg):
        logo = 'datab\\graphic\\Kivy_logo.ico'
        Notifier().show_toast(title, msg, icon_path=logo, threaded=True)
        
    def get_value(self, value):
        with open(self.PATH,'r') as f:
            js = json.load(f)
            f.close()
            if value == 'keys':
                try: 
                    return list(range(len(js)))
                except (AttributeError,ValueError,KeyError):
                    return None
            try:
                return js[value]
            except (AttributeError,ValueError,KeyError):
                return None
        
    def get_langauge(self):
        from datab.env_vars import LANGS
        return LANGS[self.get_settings()['lang']]

    def get_data(self) -> dict:
        if self.data == {}:
            if os.path.isfile(self.PATH):
                with open(self.PATH,'r') as f:
                    js = json.load(f)
                    database.data = js
                    f.close()
        
        return database.data
    
    def set(self, key, value, *args) -> bool:
        if database.settings == {}:
            database.settings = database().get_settings()
        sets = database.settings
        sets[key] = value
        import configparser
        cfg = configparser.ConfigParser()
        cfg.read('datab\\.config')
        if isinstance(value, bool):
            value = list(self.bools.keys())[list(self.bools.values()).index(value)]
        cfg.set('user_settings', key, value)
        with open('datab\\.config', 'w') as configfile:
            cfg.write(configfile)
        if key == 'start_with_windows':
            self.manage_winreg() # Apply winreg changes
        database().initiallize(database().load_cfg)

    def manage_aut(self, aut_id, key, value):
        if database.data == {}:
            database.data = database().get_data()
        cards = database.data
        cards[aut_id][key] = value
        database().save_data(data=cards)
        return value

    def save_data(self, **kwargs):
        with open(self.PATH, 'w') as f:
            json.dump(kwargs.get('data'), f, indent=6, ensure_ascii=False)
            f.close()
        try:
            if kwargs.get('close') != True:
                pass
        except ValueError:
            pass

    def get_settings(self, *args) -> dict:
        import configparser
        try:
            if database.settings != {}:
                return database.settings['user_settings']
        except AttributeError:
            pass
        database.settings = dict()
        cfg = configparser.ConfigParser()
        cfg.read('datab\\.config')
        for sect in cfg.sections():
            database.settings[sect] = dict()
            for k,v in cfg.items(sect):
                if v in self.bools:
                    v = self.bools[v]
                database.settings[sect][k] = v
        return database.settings['user_settings']
    
    def load_cfg(self, *args):
        import sys
        database().get_settings()
        if (not database.settings['user_settings']['systray_active'] or '-No-SysTray' in sys.argv):
            os.environ['NO_SYSTRAY'] = '1'
        else:
            os.environ['NO_SYSTRAY'] = '0'
        os.environ['Audio_playing'] = '0'
        if database.settings['user_settings']['notify_on_close']:
            os.environ['NOTIFY'] = '1'
        else:
            os.environ['NOTIFY'] = '0'
        if database.settings['user_settings']['hide_on_close']:
            os.environ['HIDE_ON_CLOSE'] = '1'
        else:
            os.environ['HIDE_ON_CLOSE'] = '0'
        return database.settings['user_settings']

    def configure(self):
        pass
