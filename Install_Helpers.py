import os, sys
from urllib import request
from core.exceptions import DependencesFail

def _check_pip():
        import subprocess
        try:
            process = subprocess.Popen(['pip','-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            if not input('pip not found, would you to install automatically? [y/n] ') == 'n':
                _pip = 'https://bootstrap.pypa.io/get-pip.py'
                request.urlretrieve(_pip, os.path.join(os.path.dirname(__file__), '_get_pip_temp_.py'))
                import _get_pip_temp_
                _get_pip_temp_.main()
            os.remove('_get_pip_temp_.py')

try:
    from libs.LibWin import IconStatusIter, get_admin_rights
except DependencesFail:
    _check_pip()

    if os.system('pip install pywin32') == 1:
        print('something went wrong by installing pywin32 module, install manually pywin32 to continue')

    if os.system('pip install rich') == 1:
        print('something went wrong by installing rich module, install manually rich to continue')
    
    if os.system('pip install requests') == 1:
        print('something went wrong by installing requests module, install manually requests to continue')
    
    path = sys.argv[0]
    os.system('{} {} {}'.format(sys.executable, path, sys.argv[0:]))

from rich.console import Console

if os.path.isfile('_get_pip_temp_.py'):
    os.remove('_get_pip_temp_.py')
#get_admin_rights()

class Installation_Helper:

    def __init__(self, mode='baselib', ffmpeg=False, ffmpeg_type='essential', libav=False, libav_version='11.3') -> None:

        Installation_Helper.mode = mode
        Installation_Helper._ffmpeg = ffmpeg
        Installation_Helper._ffmpeg_type = ffmpeg_type
        Installation_Helper._libav = libav
        Installation_Helper._libav_version = libav_version

        class PythonVersionNotSUpported(BaseException):
            pass

        #Python Version
        P_VERSION = sys.version[:3]

        if not (3.6 <= float(P_VERSION) and float(P_VERSION) <= 3.9):
            raise PythonVersionNotSUpported(
                'Python version {} not supported by Automator. (interpreter at {})'.format(P_VERSION, sys.executable)
                )

        _check_pip()        

        from ctypes import windll
        hwnd = windll.kernel32.GetConsoleWindow()
        if windll.user32.IsWindowVisible(hwnd):
            windll.user32.SetWindowLongA(hwnd, -16, 12582912 | 0 | 131072 | 524288) #disable resize
            windll.user32.ShowWindow(hwnd, 1)

    class Downloader:

        def __init__(self) -> None:
            Installation_Helper.Downloader.path = ''

        def _ffmpeg(self):

            if Installation_Helper._ffmpeg_type == 'essential' or Installation_Helper._ffmpeg_type == '':
                self.url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z'
            elif Installation_Helper._ffmpeg_type == 'full':
                self.url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z'

            import win32gui, win32api, time

            win32api.SetConsoleTitle('Downloader')
            time.sleep(.1)
            hWnd = win32gui.FindWindow(None, 'Downloader')

            ici = IconStatusIter
            ici().init(None, hWnd)
            r = requests.get(self.url, stream=True)
            chunk = int()
            progress = True
            total_length = 1

            if self.url.find('/'):
                Installation_Helper.Downloader.path = os.path.realpath(self.url.rsplit('/', 1)[1])
            
            if not os.path.isfile(Installation_Helper.Downloader.path):
                with open(Installation_Helper.Downloader.path, 'wb') as f:
                    try:
                        total_length = int(r.headers.get('content-length'))
                        ici().setProgress(0, total_length)
                    except TypeError:
                        ici().setBusy(True)
                        progress = False

                    for data in r.iter_content(chunk_size=1024):
                        size = f.write(data)
                        chunk += size
                        if progress:
                            ici().setProgress(chunk, total_length)
                            display_progress(chunk, total_length+1, 'Downloaded {} MB of {} MB'.format(round(chunk / 1024 / 1024, 2), round(total_length / 1024 /1024, 2)))
                        else:
                            display_progress(0, 1, 'Downloaded {} MB of {} MB'.format(round(chunk / 1024 / 1024, 2), round(total_length / 1024 /1024, 2)))
                display_progress(1,1, 'Download ended')
                ici().quit()
                del ici

        def _libav(self):
            import platform

            try:
                _arch = ''.join(list(platform.machine())[-2:])
            except IndexError:
                _arch = '32'
            _version = Installation_Helper._libav_version
            if not _version in ['11.3', '10.6', '9.18', '0.8.17']:
                _version = '11.3'

            self.url = 'http://builds.libav.org/windows/release-gpl/libav-{}-win{}.7z'.format(_version, _arch)

            import win32gui, win32api, time

            win32api.SetConsoleTitle('Downloader')
            time.sleep(.1)
            hWnd = win32gui.FindWindow(None, 'Downloader')

            ici = IconStatusIter
            ici().init(None, hWnd)
            r = requests.get(self.url, stream=True)
            chunk = int()
            progress = True
            total_length = 1

            if self.url.find('/'):
                Installation_Helper.Downloader.path = os.path.realpath(self.url.rsplit('/', 1)[1])
            
            if not os.path.isfile(Installation_Helper.Downloader.path):
                with open(Installation_Helper.Downloader.path, 'wb') as f:
                    try:
                        total_length = int(r.headers.get('content-length'))
                        ici().setProgress(0, total_length)
                    except TypeError:
                        ici().setBusy(True)
                        progress = False

                    for data in r.iter_content(chunk_size=1024):
                        size = f.write(data)
                        chunk += size
                        if progress:
                            ici().setProgress(chunk, total_length)
                            display_progress(chunk, total_length+1, 'Downloaded {} MB'.format(round(chunk / 1024 / 1024, 2), round(total_length / 1024 /1024, 2)))
                        else:
                            display_progress(0, 1, 'Downloaded {} MB'.format(round(chunk / 1024 /1024, 2), round(total_length / 1024 /1024, 2)))
                display_progress(1,1, 'Download ended')

    def install(self):
        _skip = False
        os.environ['KIVY_NO_ARGS'] = '1'
        os.environ['KIVY_NO_CONSOLELOG'] = '1'
        # Python comtypes doesn't work with setuptools 60.0 so downgade it!
        _skip_setuptools = False
        try:
            import setuptools
            if float('.'.join(setuptools.__version__.split('.')[:1])) <= 57.0:
                _skip_setuptools = True
        except ImportError:
            pass

        if not _skip_setuptools:
            _setuptools = ['setuptools==57.0.0', 'wheel==0.36.2']
            for i in _setuptools:
                os.system('{} -m pip install --no-cache-dir {}'.format(sys.executable, i))

        # now start to download required pakages
        if Installation_Helper.mode == 'build-tool':
            pakages = open(os.path.realpath('requirements_win32.txt'), 'r').read().split('\n\n')[1].split('\n')
        elif Installation_Helper.mode == 'all':
            pakages = open(os.path.realpath('requirements_win32.txt'), 'r').read().split('\n')
        elif Installation_Helper.mode == 'baselib' or self.mode == '':
            pakages = open(os.path.realpath('requirements_win32.txt'), 'r').read().split('\n\n')[0].split('\n')
        elif Installation_Helper.mode == 'skip':
            _skip = True
        else:
            return

        if not _skip:
            # check the missing pakages
            missing = list()

            for i in pakages:
                if i.startswith('#') or i == '':
                    pass
                else:
                    try:
                        exec('import {}'.format(i))
                    except (ModuleNotFoundError, ImportError):
                        #exceptions might be pakage names different than pip tag
                        if i == 'pywin32':
                            try:
                                import pywin
                            except (ModuleNotFoundError, ImportError):
                                missing.append(i)
                        elif 'kivy.' in i:
                            i = i.replace('kivy.', 'kivy_')
                            try:
                                exec('import %s' % i)
                            except (ModuleNotFoundError, ImportError):
                                missing.append(i)
                        else:
                            missing.append(i)
                    except Exception as e:
                        if os.environ.get('DEBUG'):
                            print(e)

            # install missing pakages
            if len(missing) > 0:
                for i in missing:
                    os.system('pip install {}'.format(i))
            else:
                print('all the dipendences are already installed')
                os.system('pause')

        try:
            import py7zr
            from py7zr.exceptions import Bad7zFile
        except (ModuleNotFoundError, ImportError):
            if input('the py7zr module is missing, Automator will temporary install this module.\nProceed? (y/n)') == 'y':
                os.system('python -m pip install py7zr')
                import py7zr
                from py7zr.exceptions import Bad7zFile
            else:
                print('FFmpeg installation skipped.')
                return

        if self._ffmpeg:

            for i in os.environ['PATH'].split(';'):
                if 'ffmpeg\\bin' in i:
                    print('FFmpeg is already installed on your system!')
                    os.system('pause')
                    exit(0)

            Installation_Helper.Downloader()._ffmpeg()
            print('Extracting "{}" under "{}"'.format(Installation_Helper.Downloader.path, os.path.realpath(Installation_Helper.Downloader.path.split('.')[0])))

            try:
                archive = py7zr.SevenZipFile(os.path.realpath(Installation_Helper.Downloader.path), mode='r')
                try:
                    archive.extractall(os.path.realpath(Installation_Helper.Downloader.path.split('.')[0]))
                except TypeError:
                    pass
                archive.close()
            except Bad7zFile:
                print('Bad 7z file, re download it.')
                os.remove(os.path.realpath(Installation_Helper.Downloader.path))
                Installation_Helper.Downloader()._ffmpeg()
                archive = py7zr.SevenZipFile(os.path.realpath(Installation_Helper.Downloader.path), mode='r')
                try:
                    archive.extractall(os.path.realpath(Installation_Helper.Downloader.path.split('.')[0]))
                except TypeError:
                    pass
                archive.close()

            print('Setting up ffmpeg...', end='\r')

            os.system('start /wait /min cmd /c "{} & cd %windir%\\system32 & setx /m PATH "{}\\{}\\bin;%PATH%""'.format(os.environ['windir'].split('\\')[0], os.path.realpath(Installation_Helper.Downloader.path.split('.')[0]), 
            os.listdir(os.path.realpath(Installation_Helper.Downloader.path.split('.')[0]))[0]))
            print('Setting up ffmpeg... done')
            
            
        if self._libav:
            Installation_Helper().Downloader()._libav()
            print('Extracting "{}" under "{}"'.format(Installation_Helper.Downloader.path, os.path.realpath(Installation_Helper.Downloader.path.split('.')[0])))

            try:
                archive = py7zr.SevenZipFile(os.path.realpath(Installation_Helper.Downloader.path), mode='r')
                try:
                    archive.extractall(os.path.realpath(Installation_Helper.Downloader.path.split('.')[0]))
                except TypeError:
                    pass
                archive.close()
            except Bad7zFile:
                print('Bad 7z file, re download it.')
                os.remove(os.path.realpath(Installation_Helper.Downloader.path))
                Installation_Helper.Downloader()._libav()
                archive = py7zr.SevenZipFile(os.path.realpath(Installation_Helper.Downloader.path), mode='r')
                try:
                    archive.extractall(os.path.realpath(Installation_Helper.Downloader.path.split('.')[0]))
                except TypeError:
                    pass
                archive.close()

def display_progress(iteration, total, process):
    bar_max_width = 40 
    bar_current_width = bar_max_width * iteration // total
    bar = "█" * bar_current_width + "-" * (bar_max_width - bar_current_width)
    progress = "%.1f" % (iteration / total * 100)
    Console().print(f"|{bar}| {progress} % {process}                     ", end="\r")
    if iteration == total:
        print('\n')
