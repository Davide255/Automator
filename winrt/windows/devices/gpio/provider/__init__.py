# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.210202.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.Devices.Gpio.Provider")

try:
    import winrt.windows.foundation
except:
    pass

try:
    import winrt.windows.foundation.collections
except:
    pass

class ProviderGpioPinDriveMode(enum.IntEnum):
    INPUT = 0
    OUTPUT = 1
    INPUT_PULL_UP = 2
    INPUT_PULL_DOWN = 3
    OUTPUT_OPEN_DRAIN = 4
    OUTPUT_OPEN_DRAIN_PULL_UP = 5
    OUTPUT_OPEN_SOURCE = 6
    OUTPUT_OPEN_SOURCE_PULL_DOWN = 7

class ProviderGpioPinEdge(enum.IntEnum):
    FALLING_EDGE = 0
    RISING_EDGE = 1

class ProviderGpioPinValue(enum.IntEnum):
    LOW = 0
    HIGH = 1

class ProviderGpioSharingMode(enum.IntEnum):
    EXCLUSIVE = 0
    SHARED_READ_ONLY = 1

GpioPinProviderValueChangedEventArgs = _ns_module.GpioPinProviderValueChangedEventArgs
IGpioControllerProvider = _ns_module.IGpioControllerProvider
IGpioPinProvider = _ns_module.IGpioPinProvider
IGpioProvider = _ns_module.IGpioProvider