import time, os

#Audio Requirements
from ctypes import POINTER, cast

from os import environ
from threading import Thread

class Audio:

    '''
    '''

    class Controller:
        class Process:
            def Process(self, process_name):
                if process_name != None:
                    self.process_name = process_name
                    self.volume = self.process_volume()

            def mute(self):
                from libs.PyCAW import AudioUtilities
                try:
                    from kivy.logger import Logger
                except ImportError:
                    import logging as Logger
                sessions = AudioUtilities.GetAllSessions()
                for session in sessions:
                    interface = session.SimpleAudioVolume
                    if session.Process and self.process_name in session.Process.name():
                        interface.SetMute(1, None)
                        Logger.info('Audio:', self.process_name, 'has been muted.')

            def unmute(self):
                from libs.PyCAW import AudioUtilities
                try:
                    from kivy.logger import Logger
                except ImportError:
                    import logging as Logger
                sessions = AudioUtilities.GetAllSessions()
                for session in sessions:
                    interface = session.SimpleAudioVolume
                    if session.Process and self.process_name in session.Process.name():
                        interface.SetMute(0, None)
                        Logger.info('Audio:', self.process_name, 'has been unmuted.')

            def process_volume(self):
                from libs.PyCAW import AudioUtilities
                try:
                    from kivy.logger import Logger
                except ImportError:
                    import logging as Logger
                sessions = AudioUtilities.GetAllSessions()
                for session in sessions:
                    interface = session.SimpleAudioVolume
                    if session.Process and session.Process.name() == self.process_name:
                        Logger.info('Audio: Volume:', interface.GetMasterVolume())
                        return interface.GetMasterVolume()

        def setMasterLevel(self, level:float):
            if isinstance(level, int):
                level = level/100
            from comtypes import CLSCTX_ALL
            from libs.PyCAW import AudioUtilities, IAudioEndpointVolume
            interface = AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level, None)

    async def async_initiallize(self):
        from winrt.windows.media.playback import MediaPlayer
        Audio.mediaplayer = MediaPlayer()

    def _menu_voices(self, state:bool):
        try:
            from libs.LibWin import SysTrayIcon
        except OSError:
            return False
        if state:
            Audio_voices = ("Play/Pause Audio", None, Audio().stop_play_audio),  ("Close Audio", None, Audio().quit_audio)
        else:
            Audio_voices = ("Play/Pause Audio", None, SysTrayIcon.Item_Deactivate),  ("Close Audio", None, SysTrayIcon.Item_Deactivate),
        for i in Audio_voices:
            SysTrayIcon().EditMenuItemInfo(i[0],i)      

    async def _play_audio(self, filename, keep_alive: bool = True):
        from winrt.windows.media.playback import MediaPlaybackItem, MediaPlaybackState
        from winrt.windows.media import core, MediaPlaybackType
        from winrt.windows.storage import StorageFile
        import asyncio
        await asyncio.create_task(self.async_initiallize())
        item = MediaPlaybackItem(core.MediaSource.create_from_storage_file(await StorageFile.get_file_from_path_async(filename)))
        self.mediaplayer.source = item
        self.mediaplayer.add_media_ended(self.media_ended)
        self.mediaplayer.play()

        #update the display proprieties
        props = item.get_display_properties()
        props.type = MediaPlaybackType.MUSIC
        props.music_properties.title = os.path.basename(filename)
        item.apply_display_properties(props)

        if keep_alive:
            try:
                session = self.mediaplayer.playback_session
                while session != MediaPlaybackState.NONE:
                    session = self.mediaplayer.playback_session
                    time.sleep(2)
                return
            except RuntimeError:
                return

    class StopMusic(BaseException):
        pass

    def media_ended(self, *args):
        self.quit()

    def quit(self):
        self.mediaplayer.close()

    def play(self):
        self.mediaplayer.play()
        
    def pause(self):
        self.mediaplayer.pause()
        
    def _show_song_metas(self):
        'Internal function work in progress'
        import audio_metadata
        import win32con
        import win32gui
        meta = audio_metadata.load(environ['AUDIO_PATH'])
        print(meta)
        meta_tags = meta.tags
        metas = {}
        cat = ['artist', 'album', 'bmp', 'date', 'genre']
        
        for i in meta_tags:
            if i in cat:
                metas[i] = meta_tags[i]
            else:
                metas[i] = 'None'

        meta_str = """artist: {}
        album: {}
        bpm: {}
        year: {}
        genre: {}
        duration: {}
        
        Others:

        bitrate: {}
        bit_depth:
        simple rate: {}""".format(metas['artist'], metas['album'], metas['bpm'], metas['date'], metas['genre'], 
                                  meta.streaminfo['duration'], meta.streaminfo['bitrate'], meta.streaminfo['bit_depth'], meta.streaminfo['simple_rate'])

        win32gui.MessageBox(None, meta_str, "Song Meta", win32con.MB_OK | win32con.IDI_INFORMATION)

    def show_song_metas(self, threadded=True):

        return
        if threadded:
            th = Thread(target=self._show_song_metas, daemon=True)
            th.start()
            Logger.debug('Audio: audio thread started at {} with ident {}'.format(datetime.now(), th.ident))
        else:
            self._show_song_metas()
            Logger.debug('Audio: audio started at {}'.format(datetime.now()))

    def play_audio(self, filename, threadded=True):
        import asyncio
        try:
            from kivy.logger import Logger
        except ImportError:
            import logging as Logger
        from datetime import datetime
        #: Union[str, bytes, PathLike[str], PathLike[bytes], IO]
        #: Optional[str] 
        if threadded:
            asyncio.run(self._play_audio(filename, False))
            Logger.debug('Audio: audio started at {}'.format(datetime.now()))
        else:
            asyncio.run(self._play_audio(filename))
            Logger.debug('Audio: audio started at {}'.format(datetime.now()))

    class NotSupportedFile(BaseException):
        pass
    
    class Queue:

        def __init__(self, queue_definition: object, random: bool = True, repeat: int = 0, threadded: bool = False, daemon: bool = None, **t_kwargs) -> None:
            '''
            Play a music Queue
            ==================
            
            simple usage:

                Select music from a list:
                >>> from audio import Audio
                >>> Audio.Queue(['file1.mp3', 'some\\dir\\file2.mp3'])

                select a music from a file:
                >>> from audio import Audio
                >>> Audio.Queue(file.txt or file.json) #see options to know file format

                select music from a folder:
                >>> from audio import Audio
                >>> folder = Audio.Queue.Folder('C:\\Users\\david\\Music\\Dede')
                >>> Audio.Queue(folder)

            options:

              queue_definition:
                
                the list of files name that must be:
                - list
                - file with .read() support
                - .json file like {"queue":[somefiles]}
                - Queue.Folder object

              random:

                ramdom choose the order of audios

              threadded (for advanced users):

                Start a thread as Queue manager, with this option you have the full control of queue function:
                for example, stopping a queue:

                >>> from audio import Audio
                >>> Audio.Queue(['file1.mp3', 'some\\dir\\file2.mp3'])
                >>>  
                >>> while True: # <- Leave the process open
                >>>     if input() == '':  # <- on enter press
                >>>         Audio.Queue.quit()  #<- do not pass self parameter
                >>>         break  #<- interrupt the main loop

                other options:
                
                !!! DON'T PASS ANY PARAMETER !!!

                Audio.Queue.next()      play the next song on in the list
                Audio.Queue.provious()  play the previous song in the list


            '''
            import asyncio
            asyncio.run(Audio().async_initiallize())
            if threadded:
                asyncio.run(self.play_queue_mp(queue_definition, random, repeat, False))
            else:
                asyncio.run(self.play_queue_mp(queue_definition, random, repeat))

        async def play_queue_mp(self, queue_definition: object, random: bool = False, repeat: int = 0, keep_alive: bool = True):
            from winrt.windows.media.playback import MediaPlaybackItem, MediaPlaybackList, MediaPlaybackState
            from winrt.windows.media import core, MediaPlaybackType
            from winrt.windows.storage import StorageFile
            try:
                if environ['queue_playing'] == '1':
                    try:
                        from kivy.logger import Logger
                    except ImportError:
                        import logging as Logger
                    Logger.warning('A queue from automator is already playing. End it to start a new one')
                    return
                else:
                    environ['queue_playing'] = '1'
            except KeyError:
                environ['queue_playing'] = '1'

            try:
                queue = queue_definition.read()
                queue = queue.split('\n')
            except (IOError, OSError, AttributeError):
                if isinstance(queue_definition, str):
                    try:
                        suffix = os.path.basename(queue_definition).split('.')[1]
                        if not os.path.isfile(queue_definition):
                            raise FileNotFoundError('file {} not found!'.format(queue_definition))
                    except IndexError:
                        raise Audio.NotSupportedFile('extension is not supported')

                    if suffix == 'json':
                        from json import load
                        js = load(open(queue_definition, 'r'))
                        queue = js['queue']
                    elif suffix == 'txt':
                        file = open(queue_definition, 'r')
                        queue = file.read().split('\n')
                        file.close()
                elif isinstance(queue_definition, list):
                    queue = queue_definition
                elif isinstance(queue_definition, self.Folder):
                    queue = [os.path.join(self.Folder.folder, f) for f in os.listdir(self.Folder.folder) if os.path.isfile(os.path.join(self.Folder.folder, f))]


            Audio.Queue._list = MediaPlaybackList()
            Audio.Queue._list.shuffle_enabled = random
            file_list = {}
            for i in queue:
                f = await StorageFile.get_file_from_path_async(i)
                file_list[i] = f
            
            for f in file_list:
                metas = os.path.basename(f).split(' - ')
                if len(metas) > 1:
                    artist = metas[0]
                    title = metas[1].split('.')[0]
                else:
                    artist = ''
                    title = metas[0].split('.')[0]
                _item = MediaPlaybackItem(core.MediaSource.create_from_storage_file(file_list[f]))
                prop = _item.get_display_properties()
                prop.type = MediaPlaybackType.MUSIC
                prop.music_properties.title = title
                prop.music_properties.artist = artist
                _item.apply_display_properties(prop)
                Audio.Queue._list.items.append(_item)

            Audio.mediaplayer.source = Audio.Queue._list
            Audio.mediaplayer.play()
            if keep_alive:
                try:
                    session = Audio.mediaplayer.playback_session
                    while session != MediaPlaybackState.NONE:
                        session = Audio.mediaplayer.playback_session
                        time.sleep(2)
                    return
                except (RuntimeError, KeyboardInterrupt):
                    Audio().quit()

        def _menu_voices(state:bool):
            from libs.LibWin import SysTrayIcon
            if state:
                Audio_voices = ("Play/Pause Audio", None, Audio().stop_play_audio),  ("Close Audio", None, Audio().quit_audio)
            else:
                Audio_voices = ("Play/Pause Audio", None, SysTrayIcon.Item_Deactivate),  ("Close Audio", None, SysTrayIcon.Item_Deactivate),
            SysTrayIcon().EditMenuItemInfo('Audio',('Audio', None, SysTrayIcon.SubMenu(Audio_voices)))

        def next():
            Audio.Queue._list.move_next()

        def previous():
            Audio.Queue._list.move_previous()

        def pause():
            Audio().pause()

        def play():
            Audio().play()

        def quit():
            Audio().quit()
            return

        class Folder:
            folder = None
            def __init__(self, folder) -> None:
                Audio.Queue.Folder.folder = folder
