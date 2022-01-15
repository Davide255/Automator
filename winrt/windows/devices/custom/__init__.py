# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.210202.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.Devices.Custom")

try:
    import winrt.windows.foundation
except:
    pass

try:
    import winrt.windows.storage.streams
except:
    pass

class DeviceAccessMode(enum.IntEnum):
    READ = 0
    WRITE = 1
    READ_WRITE = 2

class DeviceSharingMode(enum.IntEnum):
    SHARED = 0
    EXCLUSIVE = 1

class IOControlAccessMode(enum.IntEnum):
    ANY = 0
    READ = 1
    WRITE = 2
    READ_WRITE = 3

class IOControlBufferingMethod(enum.IntEnum):
    BUFFERED = 0
    DIRECT_INPUT = 1
    DIRECT_OUTPUT = 2
    NEITHER = 3

CustomDevice = _ns_module.CustomDevice
IOControlCode = _ns_module.IOControlCode
KnownDeviceTypes = _ns_module.KnownDeviceTypes
IIOControlCode = _ns_module.IIOControlCode