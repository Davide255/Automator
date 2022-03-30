from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors

class Dark_Theme_Manager:

    colors = {
        "Black":Color(0,0,0,1),
        "White":Color(1,1,1,1),
        "DefaultGray":get_color_from_hex(colors['Dark']["CardsDialogs"]),
        "CardGray":get_color_from_hex(colors['Dark']["CardsDialogs"]),
        "SwitchGray":get_color_from_hex(colors['Gray']['50'])
    }

    def __init__(self) -> None:
        from kivymd.app import MDApp
        MDApp.get_running_app().theme_cls.theme_style = 'Dark'

    def dynamic_background_canvas_rect(_widget: Widget):
        with _widget.canvas.before:
            Color(0, 0, 0, 1)
            _widget.background_rect = Rectangle()
        _widget.bind(pos=Dark_Theme_Manager._adjust_rect_pos)
        _widget.bind(size=Dark_Theme_Manager._adjust_rect_size)
        return _widget
        
    def _adjust_rect_size(widget, new_size):
        widget.background_rect.size = new_size

    def _adjust_rect_pos(widget, new_pos):
        widget.background_rect.pos = new_pos

    def White_text(_text: Widget):
        _text.theme_text_color = 'Custom'
        _text.text_color = Dark_Theme_Manager.colors['White'].rgba
        return _text

    def Dark_switch(_switch: Widget):
        _switch.theme_thumb_down_color = 'Primary'
        _switch.theme_thumb_color = 'Custom'
        _switch._set_thumb_color(Dark_Theme_Manager.colors['SwitchGray'])
        #_switch.thumb_color = Dark_Theme_Manager.colors['SwitchGray']
        #_switch._set_thumb_color(Dark_Theme_Manager.colors['SwitchGray'])  

        return _switch      
