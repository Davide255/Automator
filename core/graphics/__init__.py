from .Theme import *
from .FileChooser import *
import os

# clr initiallize all .NET classes that can be called from python just importing like in C#
if not os.environ.get('BINARY_MODE'):
    try:
        from libs.dotNET import clr
        success = True
    except ImportError:
        try:
            # clr is a namespace from the python pakage "pythonnet"
            # to install: pip install --upgrade pythonnet
            import clr
            success = True
        except ImportError:
            success = False
else:
    import clr
    success = True

if success:
    from System import Environment

    USERDIR = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)
    MUSICDIR = Environment.GetFolderPath(Environment.SpecialFolder.MyMusic)
    VIDEODIR = Environment.GetFolderPath(Environment.SpecialFolder.MyVideos)
    APPDATADIR = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData)

else:

    USERDIR = MUSICDIR = VIDEODIR = APPDATADIR = 'C:\\'

class pakedWidget():
    
    def switch(self, **kwargs):
        from kivymd.uix.selectioncontrol import MDSwitch

        sw = MDSwitch(**kwargs)
        if kwargs.get('pos_hint') == None:
            sw.pos_hint = {'center_x': .80, 'center_y': .3}
        return sw

    from kivymd.uix.card import MDCard
    from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
    class CustomCard(MDCard, RoundedRectangularElevationBehavior): 
        '''Implements a material design v3 card in kivymd >> 0.104.3'''

    def card(self, **kwargs):
        mc = self.CustomCard(**kwargs) #, style='elevated')
        if not kwargs.get('orientation'):
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
        if not kwargs.get('do_scroll_x'):
            sv.do_scroll_x = False
        if not kwargs.get('do_scroll_y'):
            sv.do_scroll_y = True
        return sv

    def gridlayout(self, **kwargs):
        from kivy.uix.gridlayout import GridLayout
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
        from kivy.uix.boxlayout import BoxLayout
        bl = BoxLayout(**kwargs)
        if not kwargs.get('orientation'):
            bl.orientation = 'vertical'
        return bl

    def toolbar(self, title, _callback = None, **kwargs):
        if kwargs.get('left_action_item_bypass') == True:
            lft_act_bypass = True
            kwargs.pop('left_action_item_bypass')
        else:
            lft_act_bypass = False
        from kivymd.uix.toolbar import MDToolbar
        tb = MDToolbar(**kwargs)
        tb.title = title
        if not lft_act_bypass:
            tb.left_action_items = [['menu', lambda x: _callback(x)]]
        return tb


def askopenfilename(**kwargs):
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    Tk().withdraw()
    return askopenfilename(**kwargs)

try:
    from datab.env_vars import START_TIME
    start_time = START_TIME
except ImportError:
    start_time = 0
from core.exceptions import StopApplication
from core import SysTrayIcon, change_text
