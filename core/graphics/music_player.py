import comtypes, os

comtypes.CoUninitialize()
try:
    from winrt import _winrt
    _winrt.init_apartment()
except RuntimeError:
    if not os.environ.get('NO_MEDIA_PLAYER_WINRT_MESSAGE'):
        print('winrt not initiallized!')

from kivymd.app import MDApp
from kivymd.uix.slider import MDSlider
from kivymd.uix.button import MDFloatingActionButton, MDIconButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.app import App
from typing import Union

try:
    from core.graphics import *
except ImportError:
    from . import *

try:
    from Automator import pakedWidget
except ImportError:
    from kivymd.uix.toolbar import MDToolbar
    class pakedWidget:
        def toolbar(self, title, **kwargs):
            if kwargs.get('left_action_item_bypass') == True:
                kwargs.pop('left_action_item_bypass')
            tb = MDToolbar(**kwargs)
            tb.title = title
            return tb

from threading import Thread

import time, os
try:
    from core.audio.Audio import Audio
except ModuleNotFoundError:
    from Audio import Audio
import asyncio, sys
if sys.version_info >= (3, 8, 0): #If python version is > than 3.8.0 asyncio must set his policy to WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Slider(MDSlider):
    def collide_point(self, x, y):
        return self.x <= x <= self.right and self.y+250 <= y <= self.top-250

class Volume_Icon(MDIconButton):
    def collide_point(self, x, y):
        return self.x <= x <= self.right and self.y+300 <= y <= self.top-300

class GUI():

    def build(self, left_actions: list = None, tree_view: Union[TreeDirectoryWidget, DirectoryWidget] = None):
        Window.bind(on_drop_file=self.on_drop_file)
        if bool(os.environ.get('FORCE_DARK')):
            try:
                MDApp.get_running_app().theme_cls.theme_style = 'Dark'
            except AttributeError:
                from kivymd.theming import ThemeManager
                self.theme_cls = ThemeManager()
                self.theme_cls.theme_style = 'Dark'
        box = MDBoxLayout(orientation = 'vertical')
        toolbar = pakedWidget().toolbar('Music Player', left_action_item_bypass=True)
        if left_actions:
            toolbar.left_action_items = left_actions
        toolbar.right_action_items = [["music-note", lambda *x: x]]
        box.add_widget(toolbar)        
        mainbox = MDBoxLayout(orientation='vertical')
        mainFrame = FloatLayout()
        
        GUI.sc = time.strftime("%M:%S", time.gmtime(Audio().get_total()))
        GUI.secs = sum(int(x) * 60 ** i for i, x in enumerate(reversed(GUI.sc.split(':'))))

        image = Image(source=os.path.realpath('datab\\graphic\\icon-music.png') if os.path.isfile(os.path.realpath('datab\\graphic\\icon-music.png')) else "D:\Automator\datab\graphic\icon-music.png")
        image.size_hint = None, None
        image.size = 325, 325
        if tree_view:
            image.pos_hint = {'center_x': .77, 'center_y': .70}
        else:
            image.pos_hint = {'center_x': .5, 'center_y': .70}
        mainFrame.add_widget(image)

        if tree_view:
            GUI.tree_view = tree_view(start_directory='music',size_hint=(.54, .60), pos_hint={'center_y':.7, 'center_x':.269})
            mainFrame.add_widget(GUI.tree_view)
        else:
            GUI.tree_view = None

        GUI.title = MDLabel(text=Audio.title if hasattr(Audio, 'title') else '', halign='center')
        GUI.title.pos_hint = {'center_x':.5, 'center_y':.35}
        mainFrame.add_widget(GUI.title)

        GUI.time_slider = Slider()
        GUI.time_slider.min=0
        GUI.time_slider.max=GUI.secs
        GUI.time_slider.hint=False
        GUI.time_slider.pos_hint = {'center_x':.5, 'center_y':.25}
        GUI.time_slider.pressed = False
        GUI.time_slider.bind(value=lambda *args: GUI().on_slider_move(args[0]))
        GUI.time_slider.bind(on_touch_down=lambda *args: self.slider_pressed(args[1]))
        GUI.time_slider.bind(on_touch_up=lambda *args: self.slider_released(args[1], args[0].value))
        mainFrame.add_widget(GUI.time_slider)

        GUI.total_time_label = MDLabel(text=GUI.sc, halign='center')
        GUI.total_time_label.pos_hint = {'center_x':.95, 'center_y':.19}
        mainFrame.add_widget(GUI.total_time_label)

        GUI.backwords_button = MDIconButton(icon='skip-backward')
        GUI.backwords_button.pos_hint = {'center_x':.43, 'center_y':.17}
        GUI.backwords_button.size_hint = None, None
        GUI.backwords_button.size = 37, 37
        GUI.backwords_button.bind(on_press=GUI.EventHandler.on_backward_button_pressed)
        GUI.backwords_button.bind(on_release=GUI.EventHandler.on_backward_button_released)
        mainFrame.add_widget(GUI.backwords_button)

        GUI.play_pause_button = MDFloatingActionButton(icon='play')
        GUI.play_pause_button.pos_hint = {'center_x':.5, 'center_y':.17}
        GUI.play_pause_button.bind(on_release=lambda *args: Audio().play_pause())
        mainFrame.add_widget(GUI.play_pause_button)

        GUI.fast_forward_button = MDIconButton(icon='skip-forward')
        GUI.fast_forward_button.pos_hint = {'center_x':.57, 'center_y':.17}
        GUI.fast_forward_button.size_hint = None, None
        GUI.fast_forward_button.size = 37, 37
        GUI.fast_forward_button.bind(on_press=GUI.EventHandler.on_forward_button_pressed)
        GUI.fast_forward_button.bind(on_release=GUI.EventHandler.on_forward_button_released)
        mainFrame.add_widget(GUI.fast_forward_button)

        GUI.current_time_label = MDLabel(text='00:00', halign='center')
        GUI.current_time_label.pos_hint = {'center_x':.05, 'center_y':.19}
        mainFrame.add_widget(GUI.current_time_label)

        volume_low_icon = Volume_Icon(icon='volume-low')
        volume_low_icon.pos_hint = {'center_x':.72, 'center_y':.085}
        mainFrame.add_widget(volume_low_icon)

        GUI.volume_slider = Slider(min=0, max=100, hint=True, step=5)
        GUI.volume_slider.value = Audio().get_volume()
        GUI.volume_slider.pos_hint = {'center_x':.84, 'center_y':.09}
        GUI.volume_slider.size_hint_x = .2
        GUI.volume_slider.bind(value=self.volume_slider_handler)
        mainFrame.add_widget(GUI.volume_slider)

        volume_high_icon = Volume_Icon(icon='volume-high')
        volume_high_icon.pos_hint = {'center_x':.95, 'center_y':.085}
        mainFrame.add_widget(volume_high_icon)

        mainbox.add_widget(mainFrame)

        box.add_widget(mainbox)
        Thread(target=self.update_widgets, daemon=True).start()
        return box

    def volume_slider_handler(self, slider, value):
        Audio().set_volume(value)

    def on_drop_file(self, window, filename, *args):
        Audio().play_audio(filename.decode('utf-8'), True)
        GUI.title.text = os.path.basename(filename.decode('utf-8')).split('.')[0]
        time.sleep(.1)
        GUI.total_time_label.text = time.strftime("%M:%S", time.gmtime(Audio().get_total()))

    def slider_pressed(self, motion):
        if GUI.time_slider.pos[1] * -1 - 20 < motion.pos[1] < GUI.time_slider.pos[1] * -1 + 20:
            GUI.time_slider.pressed = True
        else:
            GUI.time_slider.value = Audio().get_pos()

    def slider_released(self, motion, value):
        if GUI.time_slider.pos[1] * -1 - 20 < motion.pos[1] < GUI.time_slider.pos[1] * -1 + 20 or GUI.time_slider.pressed == True:
            Audio().set_pos(value)
            GUI.time_slider.pressed = False
        else:
            GUI.time_slider.value = Audio().get_pos()

    def on_slider_move(self, slider):
        self.current_time_label.text = time.strftime("%M:%S", time.gmtime(slider.value))

    def update_widgets(self):
        while True:
            if hasattr(Audio, 'mediaplayer'):
                if Audio().is_playing():
                    GUI.play_pause_button.icon = 'pause'
                else:
                    GUI.play_pause_button.icon = 'play'
                if GUI.time_slider.value != sum(int(x) * 60 ** i for i, x in enumerate(reversed(GUI.total_time_label.text.split(':')))) and GUI.time_slider.pressed == False:
                    GUI.time_slider.value = Audio().get_pos()
                time.sleep(0.1) #safe delay
            else:
                time.sleep(5)

    class EventHandler:
        def on_forward_button_pressed(self, *args, **kwargs):
            pass

        def on_forward_button_released(*args, **kwargs):
            pass
        
        def on_backward_button_pressed(*args, **kwargs):
            pass

        def on_backward_button_released(*args, **kwargs):
            pass

    def bind(self, **kwargs):
        for i in list(kwargs.keys()):
            exec('GUI.EventHandler.{} = kwargs[i]'.format(i))

class Music_Player_GUI(MDApp):
    def build(self):
        import asyncio
        asyncio.run(Audio().async_initiallize())
        Audio().play_audio('D:\\Automator\\Da Da Da.m4a', True)
        app = Screen(name='main')
        app.add_widget(GUI().build(None, None))
        self.sm = ScreenManager()
        self.sm.add_widget(app)
        return self.sm

if __name__ == '__main__':
    try:
        Music_Player_GUI().run()
    except KeyboardInterrupt:
        pass
    Audio().quit()
