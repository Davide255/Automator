# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.210202.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.Devices.HumanInterfaceDevice")

try:
    import winrt.windows.foundation
except:
    pass

try:
    import winrt.windows.foundation.collections
except:
    pass

try:
    import winrt.windows.storage
except:
    pass

try:
    import winrt.windows.storage.streams
except:
    pass

class HidCollectionType(enum.IntEnum):
    PHYSICAL = 0
    APPLICATION = 1
    LOGICAL = 2
    REPORT = 3
    NAMED_ARRAY = 4
    USAGE_SWITCH = 5
    USAGE_MODIFIER = 6
    OTHER = 7

class HidReportType(enum.IntEnum):
    INPUT = 0
    OUTPUT = 1
    FEATURE = 2

HidBooleanControl = _ns_module.HidBooleanControl
HidBooleanControlDescription = _ns_module.HidBooleanControlDescription
HidCollection = _ns_module.HidCollection
HidDevice = _ns_module.HidDevice
HidFeatureReport = _ns_module.HidFeatureReport
HidInputReport = _ns_module.HidInputReport
HidInputReportReceivedEventArgs = _ns_module.HidInputReportReceivedEventArgs
HidNumericControl = _ns_module.HidNumericControl
HidNumericControlDescription = _ns_module.HidNumericControlDescription
HidOutputReport = _ns_module.HidOutputReport
