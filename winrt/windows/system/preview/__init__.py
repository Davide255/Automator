# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.210202.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.System.Preview")

try:
    import winrt.windows.devices.sensors
except:
    pass

try:
    import winrt.windows.foundation
except:
    pass

class HingeState(enum.IntEnum):
    UNKNOWN = 0
    CLOSED = 1
    CONCAVE = 2
    FLAT = 3
    CONVEX = 4
    FULL = 5

TwoPanelHingedDevicePosturePreview = _ns_module.TwoPanelHingedDevicePosturePreview
TwoPanelHingedDevicePosturePreviewReading = _ns_module.TwoPanelHingedDevicePosturePreviewReading
TwoPanelHingedDevicePosturePreviewReadingChangedEventArgs = _ns_module.TwoPanelHingedDevicePosturePreviewReadingChangedEventArgs