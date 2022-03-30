import os, win32gui, win32con, sys

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.core.window import Window

#Widgets
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDTextButton, MDFillRoundFlatButton, \
    MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.uix.widget import Widget

from . import pakedWidget
from .Theme import Dark_Theme_Manager

from datab.database import database

class Screens:

    def __init__(self, _UI) -> None:
        Screens.UI = _UI

    class Not_Implemetnted:
        def __init__(self) -> None:
            res = win32gui.MessageBox(os.environ.get('Main_Window_hWnd'), 
                    'Questa schermata non è ancora disponibile in questa versione Pre-Release!',
                    'Not Implemeted Error',
                    win32con.MB_OK | win32con.MB_ICONINFORMATION)
            if res: #wait
                pass

    class Music_Player:

        def initiallize(self):
            if '--no-execute' in sys.argv:
                return
            from core.audio.Audio import Audio
            screen = Screens.UI.sm.get_screen('main')
            toolbar = screen.children[0].children[1]
            if hasattr(Audio, 'mediaplayer'):
                if Audio().is_playing():
                    toolbar.right_action_items = [["music-note", lambda *args: self.change_screen(1)]]
                else:
                    toolbar.right_action_items = [["music-note-off", lambda *x: x]]
            else:
                toolbar.right_action_items = [["music-note-off", lambda *x: x]]

        def change_screen(self, scr: int = 0):
            if scr:
                Screens.UI.sm.current = 'media_player'
            else:
                Screens.UI.sm.transition.direction = 'right'
                Screens.UI.sm.current = 'main'
                Clock.schedule_once(lambda *args: setattr(Screens.UI.sm.transition, 'direction', 'left'),\
                    Screens.UI.sm.transition.duration)
            
        def build(self):
            if '--no-execute' in sys.argv:
                return
            mp = Screen(name='media_player')
            from core.graphics.music_player import GUI
            GUI().bind(on_forward_button_pressed=lambda *args: print('pressed forward'))
            mp.add_widget(GUI().build(left_actions=[["keyboard-backspace", lambda *args: self.change_screen()]]))
            return mp

    class Main(Screen):

        def build(self):
            bx = pakedWidget().boxlayout()
            tb = pakedWidget().toolbar('Automator', left_action_item_bypass=True)
            bx.add_widget(tb)
            sv = Screens.UI.build_cards()
            if os.environ.get('FORCE_DARK'):
                Dark_Theme_Manager.dynamic_background_canvas_rect(sv)
            Clock.schedule_once(lambda *args: self._update(sv, tb))
            bx.add_widget(sv)

            return bx
        
        def _update(self, sv, tb):
            sv.size_hint=(1, None) 
            sv.size=(Window.width, Window.height - tb.size[1])

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
            sbx = pakedWidget().boxlayout()
            self.widgetref['box_layout'] = sbx
            gl1 = pakedWidget().gridlayout(cols=2)
            self.TitleBox = MDTextField(hint_text='Titolo', required=True, mode='fill', helper_text_mode='on_error', helper_text= "Il campo è obbligatorio")
            self.DescriptionBox = MDTextField(mode='fill', hint_text= "Descrizione (opzionale)")
            #adding a ref
            self.widgetref['title'] = self.TitleBox
            self.widgetref['subtitle'] = self.DescriptionBox
            #adding the widgets at the grid layout
            gl1.add_widget(self.TitleBox)
            gl1.add_widget(self.DescriptionBox)
            sbx.add_widget(gl1)
            gl = pakedWidget().gridlayout(cols=1, row_default_height=40, row_force_default = True)

            #creating automation chooser
            lbl = MDLabel(text='Agenti', halign='center', font_style='H6')#pos_hint={'center_x':.5,'center_y':.78},
            lbx = pakedWidget().boxlayout()
            lbx.add_widget(lbl)
            gl.add_widget(lbx)
            icb = MDFloatingActionButton(icon='plus')
            icb.pos_hint={'center_x':.5}
            icb.bind(on_release=lambda *args: self.agent_button_callback(*args))#pos_hint={'center_x':.5,'center_y':.66}, 
            self.widgetref['agent_+_button'] = icb
            icb_bx = pakedWidget().boxlayout()
            icb_bx.add_widget(icb)
            gl.add_widget(icb_bx)
            lbl= MDLabel(text='Azioni', halign='center', font_style='H6')#pos_hint={'center_x':.5,'center_y':.54}, 
            self.widgetref['actions_to_do_lbl'] = lbl
            lbx = pakedWidget().boxlayout()
            lbx.add_widget(lbl)
            gl.add_widget(lbx)
            icb = MDFloatingActionButton(icon='plus')
            icb.pos_hint={'center_x':.5}
            icb.bind(on_release=lambda *args: self.actions_to_do_button_callback(*args))#pos_hint={'center_x':.5,'center_y':.42}, 
            self.widgetref['actions_to_do_+_button'] = icb
            icb_bx = pakedWidget().boxlayout()
            icb_bx.add_widget(icb)
            gl.add_widget(icb_bx)
            sbx.add_widget(gl)
            sbx.bind(minimum_height=bx.setter('height'))
            bx.add_widget(sbx)
            bx.add_widget(BoxLayout())
            bx.bind(minimum_height=bx.setter('height'))
            if bool(os.environ.get('FORCE_DARK')):
                MDApp.get_running_app().theme_cls.theme_style = 'Dark'
                Dark_Theme_Manager.dynamic_background_canvas_rect(bx)
            #cr = pakedWidget().card(size=("700dp","60dp"), pos_hint={'center_x':.5,'center_y':.40})
            sv.add_widget(bx)
            return sv

        def select_from_dialog(self, dialog_histance=None, dialog_type=1):
            cls = pakedWidget().gridlayout(size_hint_y = None, cols = 1, row_default_height = 40, row_force_default=True)
            lbl = MDLabel(text='Aggiungi un\'Agente che attiverà la tua automazione.', halign = 'center')
            cls.add_widget(Dark_Theme_Manager.White_text(lbl) if bool(os.environ.get('FORCE_DARK')) else lbl)
            icb = MDIconButton(icon='plus')
            icb.md_bg_color = Dark_Theme_Manager.colors['White'].rgba
            icb.pos_hint={'center_x':.5}
            cls.add_widget(icb)
        
            if dialog_histance != None:
                return dialog_histance.dismiss()

            self.dialog = MDDialog(
                title='[color=#ffffff]Create new[/color]'\
                    if bool(os.environ.get('FORCE_DARK')) else 'Create new',
                size_hint= [0.5, None],
                size_hint_y = .8,
                md_bg_color = Dark_Theme_Manager.colors['CardGray'] if bool(os.environ.get('FORCE_DARK')) else None,
                type='custom',
                content_cls=cls,
                buttons = [
                    MDFillRoundFlatButton(
                                text='OK'),
                ]
            )
            self.dialog.bind(on_dismiss= lambda *args: self.modify_ui())

            return self.dialog

        def modify_ui(self, *args, **kwargs):
            fl = self.widgetref['box_layout']
            #checking if rem_widget is a string or a Widget
            if kwargs.get('rem_widget') != None:
                if isinstance(kwargs.get('rem_widget'), str):
                    fl.remove_widget(self.widgetref[kwargs.get('rem_widget')])
                else:
                    fl.remove_widget(kwargs.get('rem_widget'))
            try:
                if self.widgetref['agent_card'] == False:
                    cr = pakedWidget().card(orientation='horizontal', size=(Window.size[0]-40, 80), pos_hint={'center_x':.5,'center_y':.66})
                else:
                    Clock.unschedule(self.modify_ui)
                    return None
            except KeyError:
                cr = pakedWidget().card(orientation='horizontal', size=(Window.size[0]-40, 80), pos_hint={'center_x':.5,'center_y':.66})

            xicon = MDFloatingActionButton(icon='trash-can')
            xicon.pos_hint={'center_x':.9, 'center_y':1}
            xicon.md_bg_color = (1, 0, 0, 1)
            xicon.user_font_size='34dp'
            cr.add_widget(xicon)
            editicon = MDFloatingActionButton(icon='pencil')
            editicon.pos_hint={'center_x':.82, 'center_y':.5}
            editicon.user_font_size='34dp'
            cr.add_widget(editicon)
            
            fl.add_widget(cr)
            self.widgetref['agent_card'] = True
            Clock.unschedule(self.modify_ui)
            return None

        def agent_button_callback(self, *args):
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

            Screens.UI().build_menu('main', True)

    class Template_automation_screen:

        def dispatch(self, widget=None):
            #return Screens.Not_Implemetnted()
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

            if not Screens.UI.sm.has_screen(screen.name):
                Screens.UI.sm.add_widget(screen)
            else:
                widgets = screen.children[0]
                screen.remove_widget(widgets)
                scr = Screens.UI.sm.get_screen(self.title)
                scr.clear_widgets()
                scr.add_widget(widgets)
                if bool(os.environ.get('FORCE_DARK')):
                    MDApp.get_running_app().theme_cls.theme_style = 'Dark'
            Screens.UI.sm.current = self.title
            return None  
            
        def _empty(self):
            return Screen()

        def _build(self):
            scr = Screen(name=self.title)
            bx = pakedWidget().boxlayout()
            tb = pakedWidget().toolbar(self.title, left_action_item_bypass=True)
            tb.left_action_items = [["keyboard-backspace", lambda *args: Screens.Music_Player().change_screen()]]
            bx.add_widget(tb)
            gl = pakedWidget().gridlayout(cols=2)#, row_force_default=True, row_default_height=30)
            gl.add_widget(MDLabel(text='Title:', font_style='H6', size_hint_y=None, height=20))
            gl.add_widget(MDLabel(text='Description:', font_style='H6', size_hint_y=None, height=20))
            from kivy.uix.anchorlayout import AnchorLayout
            tbx = AnchorLayout(size_hint_y=None, anchor_x='center', anchor_y='center')
            title_text_field = MDTextField(text=self.title, multiline=False, helper_text='Write here your title', 
                                            helper_text_mode='on_focus', halign='center')
            title_text_field.font_size = 20
            title_text_field.halign = 'center'
            tbx.add_widget(title_text_field)
            #tbx.bind(minimum_height=tbx.setter('height'))
            gl.add_widget(tbx)
            description_text_field = MDTextField(text=self.subtitle, multiline=True, helper_text='Write here your description', 
                                                  helper_text_mode='on_focus')
            description_text_field.font_size = 15
            gl.add_widget(description_text_field)
            bx.add_widget(gl)
            bx.add_widget(pakedWidget().boxlayout())
            scr.add_widget(bx)
            return scr


    class Loading_Screen:
            
        def build(self):

            from kivy.uix.screenmanager import Screen
            from kivy.uix.floatlayout import FloatLayout
            from kivymd.uix.label import MDLabel

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
