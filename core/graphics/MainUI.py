import json, os, win32gui, win32con, sys
from typing import IO
from datab.database import database
from threading import Thread
import datetime, time

from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.clock import Clock
#kivy screens
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
#Widgets
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.theming import ThemeManager

from . import pakedWidget
from .Theme import Dark_Theme_Manager
from .Screens import Screens

from . import start_time, StopApplication, SysTrayIcon, change_text

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
        Window.bind(on_request_close=_hide)

        Logger.debug('GL: creo UI.sm')
        UI.sm = ScreenManager(transition=SlideTransition())

        Logger.debug('GL: aggiungo titolo e imposto i colori')
        self.title = "Automator"
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = database().get_settings()['theme_style'] \
            if database().get_settings()['theme_style'] != 'Dark' \
            else [Logger.warning('Theme: Dark theme is not aviable'), 'Light'][1] if not os.environ.get('FORCE_DARK') else \
            'Dark'
        self.theme_cls.primary_palette = "Blue"

        _Screens = Screens(self)

        Logger.debug('GL: creo main screen')
        main_screen = Screen(name='main')
        main_screen.add_widget(widget=_Screens.Main().build())

        Logger.debug('GL: creo settings screen')
        settings_screen = Screen(name='settings')
        settings_screen.add_widget(widget=_Screens.Settings().build())

        Logger.debug('GL: creo create_screen')
        create_screen = Screen(name='create_screen')
        create_screen.add_widget(widget=_Screens.Create_Screen().build())

        Logger.debug('GL: creo media_player screen')
        mp_screen = _Screens.Music_Player().build()

        Logger.debug('GL: aggiungo tutti gli schermi a UI.sm')
        self.sm.add_widget(_Screens.Loading_Screen().build())
        if mp_screen:
            self.sm.add_widget(mp_screen)
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
                "theme_text_color":"Custom" if bool(os.environ.get('FORCE_DARK')) else 'Primary',
                "text_color": Dark_Theme_Manager.colors['White'].rgba,
                "height": dp(56),
                "on_press":lambda *args: Thread(target=database().open_conf_file, daemon=True).start(),
                "on_release": lambda *args: self.menu.dismiss(), 
            },
            {
                "viewclass": "OneLineListItem",
                "text": f"Apri file delle Automazioni",
                "theme_text_color":"Custom" if bool(os.environ.get('FORCE_DARK')) else 'Primary',
                "text_color": Dark_Theme_Manager.colors['White'].rgba,
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
                "theme_text_color":"Custom" if bool(os.environ.get('FORCE_DARK')) else 'Primary',
                "text_color": Dark_Theme_Manager.colors['White'].rgba,
                "height": dp(56),
                "on_press": lambda x=f"main": self.not_save(x, True),
                "on_release": lambda *args: self.menu.dismiss(), 
             },
             {
                "viewclass": "OneLineListItem",
                "text": f"Salva ed esci",
                "theme_text_color":"Custom" if bool(os.environ.get('FORCE_DARK')) else 'Primary',
                "text_color": Dark_Theme_Manager.colors['White'].rgba,
                "height": dp(56),
                "on_press": lambda x=f"main": self.menu_save(x, True),
                "on_release": lambda *args: self.menu.dismiss(), 
             }
        ],
        #menu 2, create_screen
        [
            {
                "viewclass": "OneLineListItem",
                "text": f"Esci senza salvare",
                "theme_text_color":"Custom" if bool(os.environ.get('FORCE_DARK')) else 'Primary',
                "text_color": Dark_Theme_Manager.colors['White'].rgba,
                "height": dp(56),
                "on_press": lambda *args: self.not_save('main', True),
                "on_release": lambda *args: self.menu.dismiss(), 
             },
             {
                "viewclass": "OneLineListItem",
                "text": f"Salva ed esci",
                "theme_text_color":"Custom" if bool(os.environ.get('FORCE_DARK')) else 'Primary',
                "text_color": Dark_Theme_Manager.colors['White'].rgba,
                "height": dp(56),
                "on_press": Screens.Create_Screen().confirm,
                "on_release": lambda *args: self.menu.dismiss(), 
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
                'Unrecognized type'
                )        

        UI.menu = MDDropdownMenu(
            items=menu_items[itm],
            width_mult=4,
        )
        if bool(os.environ.get('FORCE_DARK')):
            UI.menu.background_color = Dark_Theme_Manager.colors['DefaultGray']

        if args[1] != False:
          if isinstance(args[0], str):
            self.sm.current = args[0]
          elif isinstance(args[0], int):
            screens = ['main','setting', 'create_screen']
            self.sm.current = screens[args[0]]
          else:
            raise TypeError(
                'Unrecognized type'
                )

        self.theme_cls.theme_style = 'Dark' if bool(os.environ.get('FORCE_DARK')) else 'Light'

        #Logger.info('GL: theme_style set on {}'.format(self.theme_cls.theme_style))
        return self.menu

    def build_cards(self):

        from core import exceptions

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
            if bool(os.environ.get('FORCE_DARK')):
                cr.update_md_bg_color(cr, 'Dark')
            gl.add_widget(cr)
            sv.add_widget(gl)

            return sv
        else:
            data = database().get_data()
        
        for i in keys:
            sw = pakedWidget().switch()
            sw.id = i
            Dark_Theme_Manager.Dark_switch(sw)
            sw.bind(active=lambda sw, *args: exceptions.Advises().Deactivate_Adv(sw))

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
            if bool(os.environ.get('FORCE_DARK')):
                Dark_Theme_Manager.White_text(lbl)
            cr.add_widget(lbl)
            cr.ids['title'] = lbl.text

            lbl = MDLabel(text=subtitle, text_size='10dp')
            lbl.halign = 'center'
            lbl.valign = 'center'
            if bool(os.environ.get('FORCE_DARK')):
                Dark_Theme_Manager.White_text(lbl)
            cr.add_widget(lbl)
            cr.ids['subtitle'] = lbl.text

            cr.bind(on_release=lambda *args: Screens.Template_automation_screen().dispatch(args[0]))
            if bool(os.environ.get('FORCE_DARK')):
                cr.md_bg_color = Dark_Theme_Manager.colors['CardGray']
            gl.add_widget(cr)
            cr = pakedWidget().card() #empty the variable

        lbl = MDLabel()
        lbl.text = '+'
        if bool(os.environ.get('FORCE_DARK')):
            Dark_Theme_Manager.White_text(lbl)
        lbl.halign = 'center'
        lbl.font_style = 'H2'

        cr.bind(on_release=lambda *args: UI().build_menu(2, True))
        cr.add_widget(lbl)
        if bool(os.environ.get('FORCE_DARK')):
            cr.md_bg_color = Dark_Theme_Manager.colors['CardGray']

        gl.size_hint = 1, None
        gl.bind(minimum_height=gl.setter('height'))
        gl.add_widget(cr)
        sv.add_widget(gl)

        return sv

    def stop_loading(self, *args):
        UI.sm.current= 'main'
        Screens.Music_Player().initiallize()
        UI.sm.get_screen('main').children[0].children[1].left_action_items = [['menu', lambda x: UI().callback(x)]]
        #                        boxlayout  | toolbar
        UI.sm.get_screen('create_screen').children[0].children[0].children[2].left_action_items = [['menu', lambda x: UI().callback(x)]]
        #                                 scrollview | boxlayout | toolbar
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
        if bool(os.environ.get('FORCE_DARK')):
            self.snackbar.bg_color = Dark_Theme_Manager.colors['CardGrey']
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
        self.build_menu(*args)

def eleve(*args):
    #using Windows API to raise the window for a major speed
    win32gui.ShowWindow(int(os.environ['Main_Window_hWnd']), 1)
    
def _hide(*args):
    #using Windows API to hide the window for a major speed
    if (database().get_settings()['hide_on_close'] and os.environ['NO_SYSTRAY'] != '1'):
        if '--no-execute' in sys.argv:
            Window.close()
            raise StopApplication()
        state = 0
        if os.environ['NOTIFY'] == '1':
            database().send_notification('Automator', 'Automator è ancora in esecuzione in background!')
            os.environ['NOTIFY'] = '0'
    elif (not database().get_settings()['hide_on_close'] or os.environ['NO_SYSTRAY'] == '1'):
        if '--no-execute' in sys.argv:
            Window.close()
            os._exit(0)
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
        SysTrayIcon().EditMenuItemInfo('Minimize', ("Open Automator UI", None, lambda *args: [eleve(), change_text(status=True)]))
    win32gui.ShowWindow(int(os.environ['Main_Window_hWnd']), state)
    return True     

