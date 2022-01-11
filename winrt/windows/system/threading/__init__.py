# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.210202.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.System.Threading")

try:
    import winrt.windows.foundation
except:
    pass

class WorkItemOptions(enum.IntFlag):
    NONE = 0
    TIME_SLICED = 0x1

class WorkItemPriority(enum.IntEnum):
    LOW = -1
    NORMAL = 0
    HIGH = 1

ThreadPool = _ns_module.ThreadPool
ThreadPoolTimer = _ns_module.ThreadPoolTimer