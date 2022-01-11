# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.210202.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.Media.Capture")

try:
    import winrt.windows.foundation
except:
    pass

try:
    import winrt.windows.foundation.collections
except:
    pass

try:
    import winrt.windows.graphics.directx.direct3d11
except:
    pass

try:
    import winrt.windows.graphics.imaging
except:
    pass

try:
    import winrt.windows.media
except:
    pass

try:
    import winrt.windows.media.capture.core
except:
    pass

try:
    import winrt.windows.media.capture.frames
except:
    pass

try:
    import winrt.windows.media.core
except:
    pass

try:
    import winrt.windows.media.devices
except:
    pass

try:
    import winrt.windows.media.effects
except:
    pass

try:
    import winrt.windows.media.mediaproperties
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

class CameraCaptureUIMaxPhotoResolution(enum.IntEnum):
    HIGHEST_AVAILABLE = 0
    VERY_SMALL_QVGA = 1
    SMALL_VGA = 2
    MEDIUM_XGA = 3
    LARGE3_M = 4
    VERY_LARGE5_M = 5

class CameraCaptureUIMaxVideoResolution(enum.IntEnum):
    HIGHEST_AVAILABLE = 0
    LOW_DEFINITION = 1
    STANDARD_DEFINITION = 2
    HIGH_DEFINITION = 3

class CameraCaptureUIMode(enum.IntEnum):
    PHOTO_OR_VIDEO = 0
    PHOTO = 1
    VIDEO = 2

class CameraCaptureUIPhotoFormat(enum.IntEnum):
    JPEG = 0
    PNG = 1
    JPEG_X_R = 2

class CameraCaptureUIVideoFormat(enum.IntEnum):
    MP4 = 0
    WMV = 1

class KnownVideoProfile(enum.IntEnum):
    VIDEO_RECORDING = 0
    HIGH_QUALITY_PHOTO = 1
    BALANCED_VIDEO_AND_PHOTO = 2
    VIDEO_CONFERENCING = 3
    PHOTO_SEQUENCE = 4
    HIGH_FRAME_RATE = 5
    VARIABLE_PHOTO_SEQUENCE = 6
    HDR_WITH_WCG_VIDEO = 7
    HDR_WITH_WCG_PHOTO = 8
    VIDEO_HDR8 = 9

class MediaCaptureDeviceExclusiveControlStatus(enum.IntEnum):
    EXCLUSIVE_CONTROL_AVAILABLE = 0
    SHARED_READ_ONLY_AVAILABLE = 1

class MediaCaptureMemoryPreference(enum.IntEnum):
    AUTO = 0
    CPU = 1

class MediaCaptureSharingMode(enum.IntEnum):
    EXCLUSIVE_CONTROL = 0
    SHARED_READ_ONLY = 1

class MediaCaptureThermalStatus(enum.IntEnum):
    NORMAL = 0
    OVERHEATED = 1

class MediaCategory(enum.IntEnum):
    OTHER = 0
    COMMUNICATIONS = 1
    MEDIA = 2
    GAME_CHAT = 3
    SPEECH = 4

class MediaStreamType(enum.IntEnum):
    VIDEO_PREVIEW = 0
    VIDEO_RECORD = 1
    AUDIO = 2
    PHOTO = 3

class PhotoCaptureSource(enum.IntEnum):
    AUTO = 0
    VIDEO_PREVIEW = 1
    PHOTO = 2

class PowerlineFrequency(enum.IntEnum):
    DISABLED = 0
    FIFTY_HERTZ = 1
    SIXTY_HERTZ = 2
    AUTO = 3

class StreamingCaptureMode(enum.IntEnum):
    AUDIO_AND_VIDEO = 0
    AUDIO = 1
    VIDEO = 2

class VideoDeviceCharacteristic(enum.IntEnum):
    ALL_STREAMS_INDEPENDENT = 0
    PREVIEW_RECORD_STREAMS_IDENTICAL = 1
    PREVIEW_PHOTO_STREAMS_IDENTICAL = 2
    RECORD_PHOTO_STREAMS_IDENTICAL = 3
    ALL_STREAMS_IDENTICAL = 4

class VideoRotation(enum.IntEnum):
    NONE = 0
    CLOCKWISE90_DEGREES = 1
    CLOCKWISE180_DEGREES = 2
    CLOCKWISE270_DEGREES = 3

WhiteBalanceGain = _ns_module.WhiteBalanceGain
AdvancedCapturedPhoto = _ns_module.AdvancedCapturedPhoto
AdvancedPhotoCapture = _ns_module.AdvancedPhotoCapture
AppCapture = _ns_module.AppCapture
CameraCaptureUI = _ns_module.CameraCaptureUI
CameraCaptureUIPhotoCaptureSettings = _ns_module.CameraCaptureUIPhotoCaptureSettings
CameraCaptureUIVideoCaptureSettings = _ns_module.CameraCaptureUIVideoCaptureSettings
CapturedFrame = _ns_module.CapturedFrame
CapturedFrameControlValues = _ns_module.CapturedFrameControlValues
CapturedPhoto = _ns_module.CapturedPhoto
LowLagMediaRecording = _ns_module.LowLagMediaRecording
LowLagPhotoCapture = _ns_module.LowLagPhotoCapture
LowLagPhotoSequenceCapture = _ns_module.LowLagPhotoSequenceCapture
MediaCapture = _ns_module.MediaCapture
MediaCaptureDeviceExclusiveControlStatusChangedEventArgs = _ns_module.MediaCaptureDeviceExclusiveControlStatusChangedEventArgs
MediaCaptureFailedEventArgs = _ns_module.MediaCaptureFailedEventArgs
MediaCaptureFocusChangedEventArgs = _ns_module.MediaCaptureFocusChangedEventArgs
MediaCaptureInitializationSettings = _ns_module.MediaCaptureInitializationSettings
MediaCapturePauseResult = _ns_module.MediaCapturePauseResult
MediaCaptureSettings = _ns_module.MediaCaptureSettings
MediaCaptureStopResult = _ns_module.MediaCaptureStopResult
MediaCaptureVideoProfile = _ns_module.MediaCaptureVideoProfile
MediaCaptureVideoProfileMediaDescription = _ns_module.MediaCaptureVideoProfileMediaDescription
OptionalReferencePhotoCapturedEventArgs = _ns_module.OptionalReferencePhotoCapturedEventArgs
PhotoCapturedEventArgs = _ns_module.PhotoCapturedEventArgs
PhotoConfirmationCapturedEventArgs = _ns_module.PhotoConfirmationCapturedEventArgs
VideoStreamConfiguration = _ns_module.VideoStreamConfiguration
