from ctypes import Structure, windll, c_uint, sizeof, byref
from threading import Thread

class System:
    active = False

    class LASTINPUTINFO(Structure):
        _fields_ = [
            ('cbSize', c_uint),
            ('dwTime', c_uint),
        ]

    def _get_idle_duration(self):
        self.lastInputInfo = System.LASTINPUTINFO()
        self.lastInputInfo.cbSize = sizeof(self.lastInputInfo)
        windll.user32.GetLastInputInfo(byref(self.lastInputInfo))
        self.millis = windll.kernel32.GetTickCount() - self.lastInputInfo.dwTime
        self.secs = self.millis / 1000.0

    def __init__(self) -> None:
        if self.active == False:
            th = Thread(System()._get_idle_duration)
            th.setDaemon(True)
            th.start()
            self.active = True

    def idle_timeout(self, action: list, actions_to_do: list):
        pass