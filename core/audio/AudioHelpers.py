# Library that provide support for audio streams

from core.audio.Audio import Audio
from pydub import AudioSegment
from libs.pafy import pafy

import asyncio

class Audio_Converter:
    def __init__(self, filename, _format=None) -> None:
        Audio_Converter.filename = filename
        if not _format:
            _format = Audio_Converter.filename.split('.')[-1]
        Audio_Converter.audio_stream = AudioSegment.from_file(Audio_Converter.filename, format=_format)
    
    def convert(self, output, _format=None):
        if not _format:
            _format = output.split('.')[-1]
        Audio_Converter.audio_stream.export(out_f=output, format=_format)

class Youtube_Stream:
    def __init__(self, url) -> None:
        Youtube_Stream.url = url
        asyncio.run(Audio().async_initiallize())
        Youtube_Stream.data = pafy.new(Youtube_Stream.url)

    def get_stream(self):
        Youtube_Stream.audio_stream = Youtube_Stream.data.audiostreams[Youtube_Stream.data.audiostreams.index(Youtube_Stream.data.getbestaudio())]
        Youtube_Stream.audio_stream_url = Youtube_Stream.audio_stream.url
        from winrt.windows.foundation import Uri
        from winrt.windows.media import core

        Youtube_Stream.stream = core.MediaSource.create_from_uri(Uri(Youtube_Stream.audio_stream_url))
        return Youtube_Stream.stream

    def download_video(self, video_path, silent=False, callback=None):
        payload = Youtube_Stream.data.streams[Youtube_Stream.data.audiostreams.index(Youtube_Stream.data.getbest())]

        payload.download(video_path, silent, callback)

    def download_audio(self, audio_path, silent=False, callback=None):
        payload = Youtube_Stream.data.audiostreams[Youtube_Stream.data.audiostreams.index(Youtube_Stream.data.getbestaudio())]

        payload.download(audio_path, silent, callback)
