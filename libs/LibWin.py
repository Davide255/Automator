from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# WINDOWS LIBRARY
import logging, threading, os, uuid, ctypes, subprocess, sys, locale, platform
from win32api import GetModuleHandle, GetSystemMetrics
from win32con import CW_USEDEFAULT, IDI_APPLICATION, IMAGE_ICON, LR_DEFAULTSIZE, LR_LOADFROMFILE, WM_DESTROY, WM_USER, WS_OVERLAPPED, WS_SYSMENU
from time import sleep
from ctypes import (POINTER, c_ulong, c_char_p, c_int, c_void_p)
from ctypes.wintypes import (BOOL, DWORD, HICON, WCHAR, HANDLE, HWND, HINSTANCE, HKEY, UINT)
from ctypes import windll
from enum import Enum
import win32gui
from win32gui import (RegisterWindowMessage, RegisterClass, UnregisterClass, LoadCursor, LoadIcon, LoadImage, CreateWindowEx, CreateWindow, 
                    UpdateWindow, PostMessage, PostQuitMessage, Shell_NotifyIcon, SetForegroundWindow, DestroyWindow,
                    NIM_MODIFY, NIF_ICON, NIF_INFO, NIF_MESSAGE, NIF_TIP, NIM_ADD, NIM_DELETE, NIM_MODIFY)
GetMessage = ctypes.windll.user32.GetMessageA
TranslateMessage = ctypes.windll.user32.TranslateMessage
DispatchMessage = ctypes.windll.user32.DispatchMessageA
DefWindowProc = ctypes.windll.user32.DefWindowProcA
InsertMenuItem = ctypes.windll.user32.InsertMenuItemA
TrackPopupMenu = ctypes.windll.user32.TrackPopupMenu
CreatePopupMenu = ctypes.windll.user32.CreatePopupMenu
GetCursorPos = ctypes.windll.user32.GetCursorPos
SetMenuItemInfo = ctypes.windll.user32.SetMenuItemInfoA
CreateCompatibleDC = ctypes.windll.gdi32.CreateCompatibleDC
GetDC = ctypes.windll.user32.GetDC
CreateCompatibleBitmap = ctypes.windll.gdi32.CreateCompatibleBitmap
GetSysColorBrush = ctypes.windll.user32.GetSysColorBrush
FillRect = ctypes.windll.user32.FillRect
DrawIconEx = ctypes.windll.user32.DrawIconEx
SelectObject = ctypes.windll.gdi32.SelectObject
DeleteDC = ctypes.windll.gdi32.DeleteDC
DestroyIcon = ctypes.windll.user32.DestroyIcon

'''
Function for showing taskbar effects
'''

class THUMBBUTTONMASK(Enum):
    THB_BITMAP = 0
    THB_ICON = 1
    THB_TOOLTIP = 2
    THB_FLAGS = 3

class THUMBBUTTONFLAGS(Enum):
    THBF_ENABLED = 0
    THBF_DISABLED = 1
    THBF_DISMISSONCLICK = 2
    THBF_NOBACKGROUND = 3
    THBF_HIDDEN = 4
    THBF_NONINTERACTIVE = 5

class THUMBBUTTON(ctypes.Structure):

    _fields_ = [
        ('dwMask', UINT),
        ('iId', UINT),
        ('iBitmap', UINT),
        ('hIcon', HICON),
        ('szTip', WCHAR),
        ('dwFlags', UINT)
    ]

class IconStatusIter():
    '''
    Basic Usage:
      Initiallizing knowing window name:

        >>> from LibWin import IconStatusIter
        >>> ici = IconStatusIter
        >>> ici().init('Window_name_str', None)

      Initiallizing knowing window handle:
        >>> from LibWin import IconStatusIter
        >>> ici = IconStatusIter
        >>> ici().init(None, window_handle)
        
      Usage:

        >>> ici().setProgress(done, total_length)     The progress indicator grows in size from left to right in proportion to the estimated amount
                                                      of the operation completed. This is a determinate progress indicator; a prediction is being 
                                                      made as to the duration of the operation.

        >>> ici().setBusy(bool)                       The progress indicator does not grow in size, but cycles repeatedly along the length of the 
                                                      taskbar button. This indicates activity without specifying what proportion of the progress is 
                                                      complete. Progress is taking place, but there is no prediction as to how long the operation
                                                      will take.

        >>> ici().setPause(bool)                      The progress indicator turns yellow to show that progress is currently stopped in one of the 
                                                      windows but can be resumed by the user. No error condition exists and nothing is preventing 
                                                      the progress from continuing. This is a determinate state. If the progress indicator is in the 
                                                      indeterminate state, it switches to a yellow determinate display of a generic percentage not 
                                                      indicative of actual progress.

        >>> ici().setError(bool)                      The progress indicator turns red to show that an error has occurred in one of the windows that
                                                      is broadcasting progress. This is a determinate state. If the progress indicator is in the 
                                                      indeterminate state, it switches to a red determinate display of a generic percentage not 
                                                      indicative of actual progress.

        >>> ici().quit()                              Stops displaying progress and returns the button to its normal state. Call this method with 
                                                      this flag to dismiss the progress bar when the operation is complete or canceled.
                                                      '''

    def init(self, window_name, handle ) -> None:
        logging.debug('Initiallizing IconStatusIter class')
        try:
            import comtypes.client as cc
            cc.GetModule('dlls\\taskbarlib.tlb')
            import comtypes.gen.TaskbarLib as tbl
            IconStatusIter.ITaskbarList3 = cc.CreateObject("{56FDF344-FD6D-11d0-958A-006097C9A090}", interface=tbl.ITaskbarList3)
            self.ITaskbarList3.HrInit()
            IconStatusIter.TBPF_NOPROGRESS = 0x00000000
            IconStatusIter.TBPF_INDETERMINATE = 0x00000001
            IconStatusIter.TBPF_NORMAL = 0x00000002
            IconStatusIter.TBPF_ERROR = 0x00000004
            IconStatusIter.TBPF_PAUSED = 0x00000008
        except Exception as e:
            logging.debug(e)
            '''The taskbar API is only available for Windows 7 or higher, on lower windows versions, linux or Mac it will cause an exception. 
            Ignore the exception and don't use the API'''
            self.ITaskbarList3 = None
            logging.warning('System not supported to IconStatusIter API (supported Windows 7 or higher instead of {})'.format(platform.platform()))
            

        sleep(0.05)
        if window_name is not None:
            IconStatusIter.hWnd = win32gui.FindWindow(None, window_name)

            try:
                assert self.hWnd
            except AssertionError:
                print('Window {} not found'.format(window_name))
        elif handle is not None:
            IconStatusIter.hWnd = handle
        else:
            raise AttributeError('No handle was passed')
        
        return IconStatusIter.hWnd
        
    def __enter__(self, *args, **kwargs):
        pass

    def __exit__(self, *args, **kwargs):
        pass

    def setBusy(self, busy):
        if self.ITaskbarList3 is not None and self.hWnd is not None:
            if busy:
                self.ITaskbarList3.SetProgressState(self.hWnd, self.TBPF_INDETERMINATE)
            else:
                self.ITaskbarList3.SetProgressState(self.hWnd, self.TBPF_NOPROGRESS)

    def setPause(self, pause):
        if self.ITaskbarList3 is not None and self.hWnd is not None:
            if pause:
                self.ITaskbarList3.SetProgressState(self.hWnd, self.TBPF_PAUSED)
            else:
                self.ITaskbarList3.SetProgressState(self.hWnd, self.TBPF_NORMAL)

    def setProgress(self, done, total):
        if self.ITaskbarList3 is not None and self.hWnd is not None:
            self.ITaskbarList3.SetProgressState(self.hWnd, self.TBPF_NORMAL)
            self.ITaskbarList3.SetProgressValue(self.hWnd, done, total)

    def setError(self, err):
        if self.ITaskbarList3 is not None and self.hWnd is not None:
            if err:
                self.ITaskbarList3. self.ITaskbarList3.SetProgressState(self.hWnd, self.TBPF_ERROR)
            else:
                self.ITaskbarList3.SetProgressState(self.hWnd, self.TBPF_NOPROGRESS)

    def quit(self):
        self.setBusy(False)

'''
Function to set a desktop wallpaper
'''
dll_loader = ctypes.CDLL
class Desktop_Wallpaper(dll_loader(os.path.join(os.getcwd(), 'dlls\\Desktop.dll'))):
    pass

'''
Function to push windows notification
'''

class Notifier(object):
    """
    code from win10toast
    """

    def __init__(self):
        self._thread = None

    def _show_toast(self, title, msg,
                    icon_path, duration):

        message_map = {WM_DESTROY: self.on_destroy, }

        # Register the window class.
        self.wc = win32gui.WNDCLASS()
        self.hinst = self.wc.hInstance = GetModuleHandle(None)
        self.wc.lpszClassName = str(f"PythonTaskbar {uuid.uuid4()}")  # must be a string
        self.wc.lpfnWndProc = message_map  # could also specify a wndproc.
        try:
            self.classAtom = RegisterClass(self.wc)
        except Exception as e:
            print(e)

        style = WS_OVERLAPPED | WS_SYSMENU
        self.hwnd = CreateWindow(self.classAtom, "Taskbar", style,
                                 0, 0, CW_USEDEFAULT,
                                 CW_USEDEFAULT,
                                 0, 0, self.hinst, None)
        UpdateWindow(self.hwnd)
        from pkg_resources import Requirement, resource_filename
        # icon
        if icon_path is not None:
            icon_path = os.path.realpath(icon_path)
        else:
            icon_path =  resource_filename(Requirement.parse("win10toast"), "win10toast/data/python.ico")
        icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
        try:
            hicon = LoadImage(self.hinst, icon_path,
                              IMAGE_ICON, 0, 0, icon_flags)
        except Exception as e:
            logging.error("Some trouble with the icon ({}): {}"
                          .format(icon_path, e))
            hicon = LoadIcon(0, IDI_APPLICATION)

        if True: #SysTrayIcon._hwnd  != None:
            # Taskbar icon
            flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
            nid = (self.hwnd, 0, flags, WM_USER + 20, hicon, "Automator")
            Shell_NotifyIcon(NIM_ADD, nid)
            Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO,
                                        WM_USER + 20,
                                        hicon, "Balloon Tooltip", msg, 200,
                                        title))

            sleep(duration)
            DestroyWindow(self.hwnd)
            UnregisterClass(self.wc.lpszClassName, None)
        else:
            flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
            nid = (SysTrayIcon._hwnd, 0, flags, WM_USER + 20, hicon, "Automator")
            Shell_NotifyIcon(NIM_ADD, nid)
            Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO,
                                        WM_USER + 20,
                                        hicon, "Balloon Tooltip", msg, 200,
                                        title))
        return None

    def show_toast(self, title="Notification", msg="Here comes the message",
                    icon_path=None, duration=5, threaded=False):

        if not threaded:
            self._show_toast(title, msg, icon_path, duration)
        else:
            if self.notification_active():
                # We have an active notification, let is finish so we don't spam them
                return False

            self._thread = threading.Thread(target=self._show_toast, args=(title, msg, icon_path, duration))
            self._thread.start()
        return True

    def notification_active(self):
        """See if we have an active notification showing"""
        if self._thread != None and self._thread.is_alive():
            # We have an active notification, let is finish we don't spam them
            return True
        return False

    def on_destroy(self, hwnd, msg, wparam, lparam):
        """Clean after notification ended.

        :hwnd:
        :msg:
        :wparam:
        :lparam:
        """
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)

        return None

# Constant defintions
SEE_MASK_NOCLOSEPROCESS = 0x00000040
SEE_MASK_NO_CONSOLE = 0x00008000

# Type definitions
PHANDLE = ctypes.POINTER(HANDLE)
PDWORD = ctypes.POINTER(DWORD)

class ShellExecuteInfo(ctypes.Structure):
    _fields_ = [
        ('cbSize',       DWORD),
        ('fMask',        c_ulong),
        ('hwnd',         HWND),
        ('lpVerb',       c_char_p),
        ('lpFile',       c_char_p),
        ('lpParameters', c_char_p),
        ('lpDirectory',  c_char_p),
        ('nShow',        c_int),
        ('hInstApp',     HINSTANCE),
        ('lpIDList',     c_void_p),
        ('lpClass',      c_char_p),
        ('hKeyClass',    HKEY),
        ('dwHotKey',     DWORD),
        ('hIcon',        HANDLE),
        ('hProcess',     HANDLE)]

    def __init__(self, **kw):
        super(ShellExecuteInfo, self).__init__()
        self.cbSize = ctypes.sizeof(self)
        for field_name, field_value in kw.items():
            setattr(self, field_name, field_value)

PShellExecuteInfo = POINTER(ShellExecuteInfo)

# Function definitions
ShellExecuteEx = windll.shell32.ShellExecuteExA
ShellExecuteEx.argtypes = (PShellExecuteInfo, )
ShellExecuteEx.restype = BOOL

WaitForSingleObject = windll.kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = (HANDLE, DWORD)
WaitForSingleObject.restype = DWORD

CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = (HANDLE, )
CloseHandle.restype = BOOL

"""
Function to get andmin rights
"""

def get_admin_rights(show_console=True):
    if windll.shell32.IsUserAnAdmin():
        return

    params = ShellExecuteInfo(
        fMask=SEE_MASK_NOCLOSEPROCESS | SEE_MASK_NO_CONSOLE,
        hwnd=None,
        lpVerb=b'runas',
        lpFile=sys.executable.encode('cp1252'),
        lpParameters=subprocess.list2cmdline(sys.argv).encode('cp1252'),
        nShow=int(show_console))

    if not ShellExecuteEx(ctypes.byref(params)):
        raise ctypes.WinError()

    handle = params.hProcess
    ret = DWORD()
    WaitForSingleObject(handle, -1)

    if windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(ret)) == 0:
        raise ctypes.WinError()

    CloseHandle(handle)
    sys.exit(ret.value)

"""
Function to create the SysTrayIcon

Modified module infi.SysTrayIcon https://github.com/Infinidat/infi.systray <- their GitHub

Variables and methods
"""

from win32con import *
WPARAM = ctypes.wintypes.WPARAM
LPARAM = ctypes.wintypes.LPARAM
HANDLE = ctypes.wintypes.HANDLE
if ctypes.sizeof(ctypes.c_long) == ctypes.sizeof(ctypes.c_void_p):
    LRESULT = ctypes.c_long
elif ctypes.sizeof(ctypes.c_longlong) == ctypes.sizeof(ctypes.c_void_p):
    LRESULT = ctypes.c_longlong

SZTIP_MAX_LENGTH = 128
LOCALE_ENCODING = locale.getpreferredencoding()

def encode_for_locale(s):
    """
    Encode text items for system locale. If encoding fails, fall back to ASCII.
    """
    try:
        return s.encode(LOCALE_ENCODING, 'ignore')
    except (AttributeError, UnicodeDecodeError):
        return s.decode('ascii', 'ignore').encode(LOCALE_ENCODING)

POINT = ctypes.wintypes.POINT
RECT = ctypes.wintypes.RECT
MSG = ctypes.wintypes.MSG

LPFN_WNDPROC = ctypes.CFUNCTYPE(LRESULT, HANDLE, ctypes.c_uint, WPARAM, LPARAM)

class MENUITEMINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("fMask", ctypes.c_uint),
                ("fType", ctypes.c_uint),
                ("fState", ctypes.c_uint),
                ("wID", ctypes.c_uint),
                ("hSubMenu", HANDLE),
                ("hbmpChecked", HANDLE),
                ("hbmpUnchecked", HANDLE),
                ("dwItemData", ctypes.c_void_p),
                ("dwTypeData", ctypes.c_char_p),
                ("cch", ctypes.c_uint),
                ("hbmpItem", HANDLE),
               ]

class NOTIFYICONDATA(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("hWnd", HANDLE),
                ("uID", ctypes.c_uint),
                ("uFlags", ctypes.c_uint),
                ("uCallbackMessage", ctypes.c_uint),
                ("hIcon", HANDLE),
                ("szTip", ctypes.c_char * SZTIP_MAX_LENGTH),
                ("dwState", ctypes.c_uint),
                ("dwStateMask", ctypes.c_uint),
                ("szInfo", ctypes.c_char * 256),
                ("uTimeout", ctypes.c_uint),
                ("szInfoTitle", ctypes.c_char * 64),
                ("dwInfoFlags", ctypes.c_uint),
                ("guidItem", ctypes.c_char * 16),
               ]
    if sys.getwindowsversion().major >= 5:
        _fields_.append(("hBalloonIcon", HANDLE))

def MessageHandler():
    pass

def PackMENUITEMINFO(text=None, hbmpItem=None, wID=None, hSubMenu=None, deactivate: bool=False, separator: bool=False):
    res = MENUITEMINFO()
    res.cbSize = ctypes.sizeof(res)
    res.fMask = 0
    if hbmpItem is not None:
        res.fMask |= MIIM_BITMAP
        res.hbmpItem = hbmpItem
    if wID is not None:
        res.fMask |= MIIM_ID
        res.wID = wID
    if text is not None:
        text = encode_for_locale(text)
        res.fMask |= MIIM_STRING
        res.dwTypeData = text
    if hSubMenu is not None:
        res.fMask |= MIIM_SUBMENU
        res.hSubMenu = hSubMenu
    if deactivate:
        res.fMask |= MIIM_STATE
        res.fState |= MFS_DISABLED
    else:
        res.fMask |= MIIM_STATE
        res.fState |= MFS_ENABLED
    if separator:
        res.fMask = MIIM_TYPE
        res.fType = MFT_SEPARATOR
    return res

def LOWORD(w):
    return w & 0xFFFF

def PumpMessages():
    msg = MSG()
    while GetMessage(ctypes.byref(msg), None, 0, 0) > 0:
        TranslateMessage(ctypes.byref(msg))
        DispatchMessage(ctypes.byref(msg))

def NotifyData(hWnd=0, uID=0, uFlags=0, uCallbackMessage=0, hIcon=0, szTip=""):
    szTip = encode_for_locale(szTip)[:SZTIP_MAX_LENGTH]
    res = NOTIFYICONDATA()
    res.cbSize = ctypes.sizeof(res)
    res.hWnd = hWnd
    res.uID = uID
    res.uFlags = uFlags
    res.uCallbackMessage = uCallbackMessage
    res.hIcon = hIcon
    res.szTip = szTip
    return res

class SysTrayIcon(object):
    """
    menu_options: tuple of tuples (menu text, menu icon path or None, function name)

    menu text and tray hover text should be Unicode
    hover_text length is limited to 128; longer text will be truncated

    Can be used as context manager to enable automatic termination of tray
    if parent thread is closed:

        with SysTrayIcon(icon, hover_text) as systray:
            for item in ['item1', 'item2', 'item3']:
                systray.update(hover_text=item)
                do_something(item)

    """
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]

    def show_menu(self, *args):
        if TPM_RIGHTALIGN in args:
            self._show_menu(position=TPM_RIGHTALIGN)
        else:
            self._show_menu()

    def is_alive():
        try:
            if SysTrayIcon._hwnd != None:
                return True
            else:
                return False
        except AttributeError:
            return False

    FIRST_ID = 1023

    class SubMenu:
        options = None
        def __init__(self, *menu_options) -> None:
            SysTrayIcon.SubMenu.options = list(menu_options)

    class Null:
        def __init__(self, *args) -> None:
            pass
    
    def EditMenuItemInfo(self, id: str or int, menu_options):
        if not SysTrayIcon._hwnd:
            return False
        if not SysTrayIcon._menu:
            SysTrayIcon._menu = CreatePopupMenu()
            self._create_menu(SysTrayIcon._menu, SysTrayIcon._menu_options)
        if isinstance(id, str):
            id = list(SysTrayIcon._menu_names_by_id.keys())[list(SysTrayIcon._menu_names_by_id.values()).index(id)]
        if menu_options[2] == SysTrayIcon.Item_Deactivate:
            item = PackMENUITEMINFO(menu_options[0], menu_options[1], deactivate=True)
        elif menu_options[2] == SysTrayIcon.Separator:
            item = PackMENUITEMINFO(menu_options[0], menu_options[1], separator=True)
        else:
            item = PackMENUITEMINFO(menu_options[0], menu_options[1])
        self._menu_names_by_id[id] = menu_options[0]
        SetMenuItemInfo(SysTrayIcon._menu, id, False, item)
        if menu_options[2] != SysTrayIcon._menu_actions_by_id[id]:
            SysTrayIcon._menu_actions_by_id[id] = menu_options[2]
        return True
    
    def Item_Deactivate():
        pass
    
    def Separator():
        pass

    def __init__(self,
                 icon=None,
                 hover_text=None,
                 menu_options=None,
                 on_quit=None,
                 on_lbutton_press=None,
                 on_rbutton_press=None,
                 default_menu_index=None,
                 window_class_name=None):

        try:
            self._hwnd
            return #return if main window is already crated
        except AttributeError:
            pass

        SysTrayIcon._icon = icon
        SysTrayIcon._icon_shared = False
        SysTrayIcon._hover_text = hover_text
        self._on_quit = on_quit

        if callable(on_lbutton_press) and on_lbutton_press != self.show_menu:
            self._on_lbutton = on_lbutton_press
        else:
            self._on_lbutton = None

        if callable(on_rbutton_press) and on_rbutton_press != self.show_menu:
            self._on_rbutton = on_rbutton_press
        else:
            self._on_rbutton = self.show_menu

        menu_options = menu_options or ()
        menu_options = menu_options + (('Quit', None, SysTrayIcon.QUIT),)
        SysTrayIcon._next_action_id = SysTrayIcon.FIRST_ID
        SysTrayIcon._menu_actions_by_id = set()
        SysTrayIcon._menu_names_by_id = dict()
        SysTrayIcon._menu_options = self._add_ids_to_menu_options(list(menu_options))
        SysTrayIcon._menu_actions_by_id = dict(self._menu_actions_by_id)

        window_class_name = window_class_name or ("SysTrayIconPy-%s" % (str(uuid.uuid4())))

        self._default_menu_index = (default_menu_index or 0)
        SysTrayIcon._window_class_name = window_class_name
        self._message_dict = {RegisterWindowMessage("TaskbarCreated"): self._restart,
                              WM_DESTROY: self._destroy,
                              WM_CLOSE: self._destroy,
                              WM_COMMAND: self._command,
                              WM_USER+20: self._notify}
        SysTrayIcon._notify_id = None
        self._message_loop_thread = None
        SysTrayIcon._hwnd = None
        SysTrayIcon._hicon = 0
        SysTrayIcon._hinst = None
        SysTrayIcon._window_class = None
        SysTrayIcon._menu = None
        self._sub_menu = None
        self._register_class()

    def __enter__(self):
        """Context manager so SysTray can automatically start"""
        self.start()
        return self

    def __exit__(self, *args):
        """Context manager so SysTray can automatically close"""
        self.shutdown()

    def WndProc(self, hwnd, msg, wparam, lparam):
        hwnd = HANDLE(hwnd)
        wparam = WPARAM(wparam)
        lparam = LPARAM(lparam)
        if msg in self._message_dict:
            self._message_dict[msg](hwnd, msg, wparam.value, lparam.value)
        return DefWindowProc(hwnd, msg, wparam, lparam)

    def _register_class(self):
        # Register the Window class.
        SysTrayIcon._window_class = win32gui.WNDCLASS()
        SysTrayIcon._hinst = self._window_class.hInstance = GetModuleHandle(None)
        self._window_class.lpszClassName = str(self._window_class_name)
        self._window_class.style = CS_VREDRAW | CS_HREDRAW
        self._window_class.hCursor = LoadCursor(0, IDC_ARROW)
        self._window_class.hbrBackground = COLOR_WINDOW
        self._window_class.lpfnWndProc = LPFN_WNDPROC(self.WndProc)
        RegisterClass(self._window_class)

    def _create_window(self):
        style = WS_OVERLAPPED | WS_SYSMENU
        SysTrayIcon._hwnd = CreateWindowEx(0, SysTrayIcon._window_class_name,
                                      SysTrayIcon._window_class_name,
                                      style,
                                      0,
                                      0,
                                      CW_USEDEFAULT,
                                      CW_USEDEFAULT,
                                      0,
                                      0,
                                      SysTrayIcon._hinst,
                                      None)
        os.environ['HWND'] = str(SysTrayIcon._hwnd)
        UpdateWindow(SysTrayIcon._hwnd)
        self._refresh_icon()

    def _message_loop_func(self):
        self._create_window()
        PumpMessages()

    def start(self, **kwargs):
        if SysTrayIcon._hwnd:
            return      # already started
        self._message_loop_thread = threading.Thread(target=self._message_loop_func, **kwargs)
        self._message_loop_thread.start()

    def shutdown(self):
        if not SysTrayIcon._hwnd:
            return      # not started
        PostMessage(self._hwnd, WM_CLOSE, 0, 0)
        self._message_loop_thread.join()

    def update(self, icon=None, hover_text=None):
        """ update icon image and/or hover text """
        if icon:
            self._icon = icon
            self._load_icon()
        if hover_text:
            self._hover_text = hover_text
        self._refresh_icon()

    def _add_ids_to_submenu_options(self, submenu_options):
        result = []
        for submenu_option in submenu_options:
            option_text, option_icon, option_action = submenu_option
            if callable(option_action) or option_action in SysTrayIcon.SPECIAL_ACTIONS:
                self._menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(submenu_option + (self._next_action_id,))
                self._menu_names_by_id[self._next_action_id] = option_text
            elif non_string_iterable(option_action):
                result.append((option_text,
                               option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
                self._menu_names_by_id[self._next_action_id] = option_text
            else:
                raise Exception('Unknown item', option_text, option_icon, option_action)
            self._next_action_id += 1
        SysTrayIcon.SubMenu.options = result
        return result

    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in SysTrayIcon.SPECIAL_ACTIONS:
                self._menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
                self._menu_names_by_id[self._next_action_id] = option_text
            elif isinstance(option_action, self.SubMenu):
                #self._menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
                self._next_action_id +=1
                self._add_ids_to_submenu_options(self.SubMenu.options)
            elif non_string_iterable(option_action):
                result.append((option_text,
                               option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
                self._menu_names_by_id[self._next_action_id] = option_text
            else:
                raise Exception('Unknown item', option_text, option_icon, option_action)
            self._next_action_id += 1
        return result

    def _load_icon(self):
        # release previous icon, if a custom one was loaded
        # note: it's important *not* to release the icon if we loaded the default system icon (with
        # the LoadIcon function) - this is why we assign self._hicon only if it was loaded using LoadImage
        if not self._icon_shared and self._hicon != 0:
            DestroyIcon(self._hicon)
            self._hicon = 0

        # Try and find a custom icon
        hicon = 0
        if SysTrayIcon._icon is not None and os.path.isfile(self._icon):
            icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
            icon = SysTrayIcon._icon
            hicon = SysTrayIcon._hicon = LoadImage(0, icon, IMAGE_ICON, 0, 0, icon_flags)
            self._icon_shared = False

        # Can't find icon file - using default shared icon
        if hicon == 0:
            self._hicon = LoadIcon(0, IDI_APPLICATION)
            self._icon_shared = True
            self._icon = None

    def _refresh_icon(self):
        if SysTrayIcon._hwnd is None:
            return
        if SysTrayIcon._hicon == 0:
            self._load_icon()
        if SysTrayIcon._notify_id:
            message = NIM_MODIFY
        else:
            message = NIM_ADD
        SysTrayIcon._notify_id = (self._hwnd,
                          0,
                          NIF_ICON | NIF_MESSAGE | NIF_TIP,
                          WM_USER+20,
                          self._hicon,
                          self._hover_text)
        Shell_NotifyIcon(message, SysTrayIcon._notify_id)

    def _restart(self, hwnd, msg, wparam, lparam):
        self._refresh_icon()

    def _destroy(self, hwnd, msg, wparam, lparam):
        if self._on_quit:
            self._on_quit(self)
        nid = (self._hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)  # Terminate the app.
        # TODO * release self._menu with DestroyMenu and reset the memeber
        #      * release self._hicon with DestoryIcon and reset the member
        #      * release loaded menu icons (loaded in _load_menu_icon) with DeleteObject
        #        (we don't keep those objects anywhere now)
        self._hwnd = None
        self._notify_id = None

    def _notify(self, hwnd, msg, wparam, lparam):
        if lparam == WM_LBUTTONDBLCLK:
            self._execute_menu_option(self._default_menu_index + SysTrayIcon.FIRST_ID)
        elif lparam == WM_RBUTTONUP:
            if self._on_rbutton and callable(self._on_rbutton):
                self._on_rbutton(self)
        elif lparam == WM_LBUTTONUP:
            if self._on_lbutton and callable(self._on_lbutton):
                if self._on_lbutton == SysTrayIcon.show_menu:
                    self._on_lbutton(self, TPM_RIGHTALIGN)
                else:
                    self._on_lbutton(self)
        return True

    def _show_menu(self, submenu_options=SubMenu, position=None):
        if SysTrayIcon._menu is None or isinstance(submenu_options, self.SubMenu):
            SysTrayIcon._menu = CreatePopupMenu()
            self._create_menu(SysTrayIcon._menu, self._menu_options)
            #SetMenuDefaultItem(self._menu, 1000, 0)
        p = [TPM_LEFTALIGN, TPM_RIGHTALIGN, TPM_CENTERALIGN]
        if position == None or not position in p:
            position = TPM_LEFTALIGN
        pos = POINT()
        GetCursorPos(ctypes.byref(pos))
        SetForegroundWindow(self._hwnd)
        TrackPopupMenu(SysTrayIcon._menu,
                       position,
                       pos.x,
                       pos.y,
                       0,
                       self._hwnd,
                       None)
        PostMessage(self._hwnd, WM_NULL, 0, 0)

    def _create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_action == SysTrayIcon.Item_Deactivate:
                deactivate = True
            else:
                deactivate = False
            if option_action == SysTrayIcon.Separator:
                separator = True
            else:
                separator = False

            if option_icon:
                option_icon = self._prep_menu_icon(option_icon)

            if not isinstance(option_action, SysTrayIcon.SubMenu) and option_id in self._menu_actions_by_id:
                item = PackMENUITEMINFO(text=option_text,
                                        hbmpItem=option_icon,
                                        wID=option_id,
                                        deactivate=deactivate,
                                        separator=separator)
                InsertMenuItem(menu, 0, 1, ctypes.byref(item))
            else:
                submenu = CreatePopupMenu()
                for sub_option_text, sub_option_icon, sub_option_action, sub_option_id in self.SubMenu.options[::-1]:
                    if sub_option_action == SysTrayIcon.Item_Deactivate:
                        deactivate = True
                    else:
                        deactivate = False
                    if sub_option_action == SysTrayIcon.Separator:
                        separator = True
                    else:
                        separator = False
                    item = PackMENUITEMINFO(text=sub_option_text, 
                                            hbmpItem=sub_option_icon, 
                                            wID=sub_option_id,
                                            deactivate=deactivate,
                                            separator=separator)
                    InsertMenuItem(submenu, 0, 1,  ctypes.byref(item))
                item = PackMENUITEMINFO(text=option_text,
                                        hbmpItem=option_icon,
                                        hSubMenu=submenu)
                InsertMenuItem(menu, 0, 1,  ctypes.byref(item))

    def _prep_menu_icon(self, icon):
        # First load the icon.
        ico_x = GetSystemMetrics(SM_CXSMICON)
        ico_y = GetSystemMetrics(SM_CYSMICON)
        hicon = LoadImage(0, icon, IMAGE_ICON, ico_x, ico_y, LR_LOADFROMFILE)

        hdcBitmap = CreateCompatibleDC(None)
        hdcScreen = GetDC(None)
        hbm = CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = SelectObject(hdcBitmap, hbm)
        # Fill the background.
        brush = GetSysColorBrush(COLOR_MENU)
        FillRect(hdcBitmap, ctypes.byref(RECT(0, 0, 16, 16)), brush)
        # draw the icon
        DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, DI_NORMAL)
        SelectObject(hdcBitmap, hbmOld)

        # No need to free the brush
        DeleteDC(hdcBitmap)
        DestroyIcon(hicon)

        return hbm

    def _command(self, hwnd, msg, wparam, lparam):
        id = LOWORD(wparam)
        self._execute_menu_option(id)

    def _execute_menu_option(self, id):
        menu_action = self._menu_actions_by_id[id]
        if menu_action == SysTrayIcon.QUIT:
            DestroyWindow(self._hwnd)
        else:
            menu_action(self)

def non_string_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return not isinstance(obj, str)
