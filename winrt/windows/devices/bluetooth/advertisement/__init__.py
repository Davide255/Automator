# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.210202.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.Devices.Bluetooth.Advertisement")

try:
    import winrt.windows.devices.bluetooth
except:
    pass

try:
    import winrt.windows.foundation
except:
    pass

try:
    import winrt.windows.foundation.collections
except:
    pass

try:
    import winrt.windows.storage.streams
except:
    pass

class BluetoothLEAdvertisementFlags(enum.IntFlag):
    NONE = 0
    LIMITED_DISCOVERABLE_MODE = 0x1
    GENERAL_DISCOVERABLE_MODE = 0x2
    CLASSIC_NOT_SUPPORTED = 0x4
    DUAL_MODE_CONTROLLER_CAPABLE = 0x8
    DUAL_MODE_HOST_CAPABLE = 0x10

class BluetoothLEAdvertisementPublisherStatus(enum.IntEnum):
    CREATED = 0
    WAITING = 1
    STARTED = 2
    STOPPING = 3
    STOPPED = 4
    ABORTED = 5

class BluetoothLEAdvertisementType(enum.IntEnum):
    CONNECTABLE_UNDIRECTED = 0
    CONNECTABLE_DIRECTED = 1
    SCANNABLE_UNDIRECTED = 2
    NON_CONNECTABLE_UNDIRECTED = 3
    SCAN_RESPONSE = 4

class BluetoothLEAdvertisementWatcherStatus(enum.IntEnum):
    CREATED = 0
    STARTED = 1
    STOPPING = 2
    STOPPED = 3
    ABORTED = 4

class BluetoothLEScanningMode(enum.IntEnum):
    PASSIVE = 0
    ACTIVE = 1

BluetoothLEAdvertisement = _ns_module.BluetoothLEAdvertisement
BluetoothLEAdvertisementBytePattern = _ns_module.BluetoothLEAdvertisementBytePattern
BluetoothLEAdvertisementDataSection = _ns_module.BluetoothLEAdvertisementDataSection
BluetoothLEAdvertisementDataTypes = _ns_module.BluetoothLEAdvertisementDataTypes
BluetoothLEAdvertisementFilter = _ns_module.BluetoothLEAdvertisementFilter
BluetoothLEAdvertisementPublisher = _ns_module.BluetoothLEAdvertisementPublisher
BluetoothLEAdvertisementPublisherStatusChangedEventArgs = _ns_module.BluetoothLEAdvertisementPublisherStatusChangedEventArgs
BluetoothLEAdvertisementReceivedEventArgs = _ns_module.BluetoothLEAdvertisementReceivedEventArgs
BluetoothLEAdvertisementWatcher = _ns_module.BluetoothLEAdvertisementWatcher
BluetoothLEAdvertisementWatcherStoppedEventArgs = _ns_module.BluetoothLEAdvertisementWatcherStoppedEventArgs
BluetoothLEManufacturerData = _ns_module.BluetoothLEManufacturerData