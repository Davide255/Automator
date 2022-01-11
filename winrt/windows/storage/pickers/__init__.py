# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.210202.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.Storage.Pickers")

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

class PickerLocationId(enum.IntEnum):
    DOCUMENTS_LIBRARY = 0
    COMPUTER_FOLDER = 1
    DESKTOP = 2
    DOWNLOADS = 3
    HOME_GROUP = 4
    MUSIC_LIBRARY = 5
    PICTURES_LIBRARY = 6
    VIDEOS_LIBRARY = 7
    OBJECTS3_D = 8
    UNSPECIFIED = 9

class PickerViewMode(enum.IntEnum):
    LIST = 0
    THUMBNAIL = 1

FileExtensionVector = _ns_module.FileExtensionVector
FileOpenPicker = _ns_module.FileOpenPicker
FilePickerFileTypesOrderedMap = _ns_module.FilePickerFileTypesOrderedMap
FilePickerSelectedFilesArray = _ns_module.FilePickerSelectedFilesArray
FileSavePicker = _ns_module.FileSavePicker
FolderPicker = _ns_module.FolderPicker
