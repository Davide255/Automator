import os, win32api, win32security, ctypes, sys

class Execute():
    
    def Execute(self, actions: list, action_to_do: list) -> None:
        self.actions = actions
        Execute.do = action_to_do

        agents = {'Battery':self.Battery().load,
                'Network':self.Network().load, 
                'Process':self.Process().load, 
                'Startup':lambda *args: Attuator().load(Execute.do),
                'System':self.System().load}
        
        for i in self.actions:
            if isinstance(i, list):
                for a in i:
                    return agents[a](self.actions[self.actions.index(i)])

    class Battery():

        def load(self, action: list) -> bool:
            self.batter = ['level', 'plugged', 'not_plugged']     

            for i in self.batter:
                if action[1] == i:
                    if i == self.batter[0]:
                        self.lvl = action[2]
                        self.level()
                    elif i == self.batter[1]:
                        self.plugged = True
                        self.plug()
                    elif i == self.batter[2]:
                        self.plugged = False
                        self.plug()

        def level(self):
            from core.battery import get_battery_info

            if int(get_battery_info()[0]) == int(self.lvl):
                return Attuator().load(Execute.do)
            else:
                return False

        def plug(self):
            from core.battery import get_battery_info
            if get_battery_info()[1] == self.plugged:
                return Attuator().load(Execute.do)
            else:
                return False

    class Network():
        def load(self, action: list) -> bool:
            self.net = ['is_connected']

            for i in self.net:
                if action[1] == i:
                    if i == self.net[0]:
                        self.ssid = action[2]
                        return self.is_connect()
            return False

        def is_connect(self):        
            net = self.get_connected_ssid()

            if str(net) == str(self.ssid):
                return Attuator().load(Execute.do)
            else:
                return False
        
        def get_connected_ssid(self):
            from core.process import execpowershellprocess
            ret = execpowershellprocess('(get-netconnectionProfile).Name')
            ret = ret.replace('\r', '')
            ret.split('\n')
            return ret[-1] if ret[-1] != '' else ret[-2]

    class Process():
        def load(self, action: list) -> bool:
            self.proc = ['is_running']
            self.next = lambda: Attuator().load(Execute.do)
            for i in self.proc:
                if i == self.proc[0]:
                    method = ['pid', 'name']
                    if action[2] == method[0]:
                        return self.is_running(pid=action[3])
                    else:
                        return self.is_running(name=action[3])

        def is_running(self, pid=None, name=None):
            if not hasattr(Execute.Process, 'next'):
                self.next = None
            if pid != None:
                from core import process
                for i in process.getallprocs():
                    if pid in i:
                        #print('processo con pid {} trovato'.format(self.pid))
                        if callable(self.next):
                            return self.next()
                        else:
                            return True
            elif name != None:
                import ctypes.wintypes

                Psapi = ctypes.WinDLL('Psapi.dll')
                EnumProcesses = Psapi.EnumProcesses
                EnumProcesses.restype = ctypes.wintypes.BOOL
                GetProcessImageFileName = Psapi.GetProcessImageFileNameA
                GetProcessImageFileName.restype = ctypes.wintypes.DWORD

                Kernel32 = ctypes.WinDLL('kernel32.dll')
                OpenProcess = Kernel32.OpenProcess
                OpenProcess.restype = ctypes.wintypes.HANDLE
                TerminateProcess = Kernel32.TerminateProcess
                TerminateProcess.restype = ctypes.wintypes.BOOL
                CloseHandle = Kernel32.CloseHandle

                MAX_PATH = 260
                PROCESS_TERMINATE = 0x0001
                PROCESS_QUERY_INFORMATION = 0x0400

                count = 32
                while True:
                    ProcessIds = (ctypes.wintypes.DWORD*count)()
                    cb = ctypes.sizeof(ProcessIds)
                    BytesReturned = ctypes.wintypes.DWORD()
                    if EnumProcesses(ctypes.byref(ProcessIds), cb, ctypes.byref(BytesReturned)):
                        if BytesReturned.value<cb:
                            break
                        else:
                            count *= 2
                    else:
                        import logging as log
                        log.debug("Call to EnumProcesses failed")
                        return False

                for index in range(int(BytesReturned.value / ctypes.sizeof(ctypes.wintypes.DWORD)) +1):
                    ProcessId = ProcessIds[index]
                    hProcess = OpenProcess(PROCESS_TERMINATE | PROCESS_QUERY_INFORMATION, False, ProcessId)
                    if hProcess:
                        ImageFileName = (ctypes.c_char*MAX_PATH)()
                        if GetProcessImageFileName(hProcess, ImageFileName, MAX_PATH)>0:
                            filename = os.path.basename(ImageFileName.value)
                            if filename == name.encode('utf-8'):
                                if callable(self.next):
                                    return self.next()
                                else:
                                    return True
                        CloseHandle(hProcess)
                return False
            else:
                return False

    class System():
        def load(self, action: list) -> bool:
            self._sys = ['idle_timeout', 'on_brightness']
            from core.system import System
            for i in action:
                if i == 'idle_timeout':
                    print('under development')
                    return True
                    System().idle_timeout(action, Execute.do)
                elif i == 'on_brightness':
                    import screen_brightness_control as sbc
                    if int(sbc.get_brightness(display=0)) == int(action[2]):
                        return Attuator().load(Execute.do)
                    else:
                        return False

class Attuator():
    def load(self, attuator: list) -> bool:
        self.attuator = attuator

        attuatori = {'Network':self.Network().load,
                     'Bluetooth':self.Bluetooth().load, 
                     'Process':self.Process().load, 
                     'System':self.System().load, 
                     'Audio':self.Audio().load}

        for i in self.attuator:     
            if isinstance(i, list):            
                for a in i:
                    return attuatori[a](self.attuator[self.attuator.index(i)])

    class Network():
        def load(self, attuators: list):
            from core.network import enum_aviable_networks, disconnect, connect
            self.attuators = attuators
            net = ['connect', 'disconnect', 'send_email']

            for i in net:
                if i == 'connect':
                    network = self.attuators[2]
                    out = enum_aviable_networks()
                    for i in out:
                        if network.encode('utf-8') in i:
                            if not network in self.get_connected_ssid():
                                disconnect()
                                return connect(network)
                    return False
                if i == 'disconnect':
                    disconnect()
                    return True
                if i == 'send_email':
                    self.send_email()
                    return True

        def get_connected_ssid(self):
            from core.process import execpowershellprocess
            ret = execpowershellprocess('(get-netconnectionProfile).Name')
            ret = ret.replace('\r', '')
            ret.split('\n')
            return ret[-1] if ret[-1] != '' else ret[-2]

        def send_email(self):
            print('Feature under development')

            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.application import MIMEApplication

            if isinstance(self.attuators[2], dict):
                self.data = self.attuators[2]

                msg = MIMEMultipart()
                msg['Subject'] = self.data['Subject']
                msgText = MIMEText('<b>%s</b>' % (msg['Subject']), 'html')
                msg.attach(msgText)

                try:
                    data = MIMEApplication(open(self.data['added_file']).read())
                    data.add_header('Content-Disposition', 'attachment', filename=self.data['added_file'])
                    msg.attach(data)
                except KeyError:
                    pass


                smtps = {'gmail': ['smtp.gmail.com', 587], 'outlook': ['smtp.live.com',587], 'office365': ['smtp.office365.com',587], 'yahoo mail': ['smtp.mail.yahoo.com',465], 'hotmail': ['smtp.live.com',465]}
                for i in list(smtps.keys()):
                  if i in self.data['user']:  
                    smtp, port = smtps[i]

                return None

                with smtplib.SMTP(smtp, port) as smtpObj:
                        smtpObj.ehlo()
                        smtpObj.starttls()
                        smtpObj.login(self.data['user'], self.data['password'])
                        smtpObj.sendmail(self.data['user'], self.data['dest'], msg.as_string())
                        smtpObj.quit()


    class Bluetooth():
        def load(self, attuators: list):
            from core import bluetooth
            bt = ['switch_on', 'switch_off']

            self.attuators = attuators

            for i in bt:
                if i in self.attuators[1]:
                    if i == bt[0]:
                        bluetooth.set_on()
                        return True
                    else:
                        bluetooth.set_off()
                        return True


    class Process():
        def load(self, attuators: list):
            proc = ['start', 'kill']

            self.attuators = attuators

            for i in proc:
                if i in attuators[1]:
                    if i == proc[0]:
                        return self.start()
                    else:
                        return self.kill()

        def start(self):
            if len(self.attuators) == 3:
                self.attuators.append(False)
            if self.attuators[2].endswith('.exe'):
                if (self.attuators[3] or not Execute.Process().is_running(name=os.path.basename(self.attuators[2]))): #Don't start a new process 
                                                                                                                         #if it's already started
                    os.startfile(self.attuators[2])
                return True
            return False
        
        def kill(self):
            import psutil
            if self.attuators[1] == 'pid':
                pid = self.attuators[2]
                psutil.Process(pid).kill()
                return True
            elif self.attuators[1] == 'name':
                for proc in psutil.process_iter():
                    if self.attuators[2] in proc.name():
                        psutil.Process(proc.pid).kill()
                        return True
            else:
                return False
            return True

    class Audio:
        def load(self, attuators: list):
            from core.audio.Audio import Audio
            
            aux = {'set_master_volume_level':lambda: Audio.Controller().setMasterLevel(float(int(self.attuators[2]) / 100)),
                   'mute_process':lambda: Audio.Controller.Process(self.attuators[2]).mute(),
                   'unmute_process':lambda: Audio.Controller.Process(self.attuators[2]).unmute(),
                   'stop/play_audio':self.stop_play_audio,
                   'play_audio':lambda: Audio().play_audio(self.attuators[2], True if not len(self.attuators) == 4 else self.attuators[3], threadded=True),
                   'music_queue':self.play_queue}

            self.attuators = attuators

            for i in attuators:
                #call the required function
                try:
                    if i in aux:
                        return aux[i]()
                except (KeyError, TypeError) as e:
                    print(e)
                
        def play_queue(self, *args):
            from audio.Audio import Audio
            if os.path.isdir(self.attuators[2]):
                dir = Audio.Queue.Folder(self.attuators[2])
                Audio().Queue(dir, #Pass only a Folder object, not str
                              True if self.attuators[3] else self.attuators[3], #Pass True if you want a shuffle
                              0 if self.attuators[4] else int(self.attuators[4]), #Pass an int() value for the number of repetions
                              True, True) #don't change this two True parameters
                return True
            else:
                Audio().Queue(self.attuators[2], #   Pass only an object that is NOT a folder, like: 
                                                 #   a file or a .read()-supporting file-like object
                                                 #   a list of files names
                              True if self.attuators[3] else self.attuators[3], #Pass True if you want a shuffle
                              0 if self.attuators[4] else int(self.attuators[4]), #Pass an int() value for the number of repetions
                              True, True) #don't change this two True parameters
                return True

        def stop_play_audio(self):
            from datab.env_vars import VK_MEDIA_PLAY_PAUSE
            import time, win32con
            key =  win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE)
            win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, key, 0, 0)
            time.sleep(0.2)
            win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, key, win32con.KEYEVENTF_KEYUP, 0)

    class System():
        def load(self, attuators: list):
            from libs import sbcLib
            import pyscreenshot as ImageGrab
            from datab.database import database
            cmds = {'reboot': lambda message='Rebooting', reboot=True: self.shotdown(message=message,reboot=reboot), 
                    'look': ctypes.windll.user32.LockWorkStation, 
                    'logoff': lambda: win32api.ExitWindows(0, 0), 
                    'shotdown':self.shotdown, 
                    'suspend':self.suspend, 
                    'hibernate':lambda: self.suspend(hibernate=True),
                    'set_brightness':lambda: sbcLib.fade_brightness(self.attuators[2], sbcLib.get_brightness(), 0.001),
                    'take_screenshot':lambda im = ImageGrab.grab(): im.save(self.attuators[2]),
                    'send_notification':lambda: database().send_notification(self.attuators[2]['title'], self.attuators[2]['msg']),}

            self.attuators = attuators

            for i in attuators:
                #Require the shotdown privileges
                self.GetPrivileges()
                #call the required function
                try:
                    if i in cmds:
                        cmds[i]()
                except (KeyError, TypeError) as e:
                    print(e)
                #restore the privileges
                self.AdjustPrivileges()
            return True

        def GetPrivileges(self):
            if 'win' in sys.platform:
                priv_flags = (win32security.TOKEN_ADJUST_PRIVILEGES |
                            win32security.TOKEN_QUERY)
                self.hToken = win32security.OpenProcessToken(
                    win32api.GetCurrentProcess(),
                    priv_flags)
                priv_id = win32security.LookupPrivilegeValue(
                None,
                win32security.SE_SHUTDOWN_NAME)
                self.old_privs = win32security.AdjustTokenPrivileges(
                    self.hToken,
                    0,
                    [(priv_id, win32security.SE_PRIVILEGE_ENABLED)])

        def AdjustPrivileges(self):
            if 'win' in sys.platform:
                win32security.AdjustTokenPrivileges(self.hToken,
                                                    0,
                                                    self.old_privs)
        
        def shotdown(self, machine:str=None, message:str='Shotting down', timeout:int=1, force:bool=False, reboot:bool=False):
            win32api.InitiateSystemShutdown(machine, message, timeout, force, reboot)

        def suspend(self, hibernate=False):
            if (win32api.GetPwrCapabilities()['HiberFilePresent'] == False and
                hibernate == True):
                    import warnings
                    warnings.warn("Hibernate isn't available. Suspending.")
            try:
                ctypes.windll.powrprof.SetSuspendState(not hibernate, True, False)
            except:
                # True=> Standby; False=> Hibernate
                # https://msdn.microsoft.com/pt-br/library/windows/desktop/aa373206(v=vs.85).aspx
                win32api.SetSystemPowerState(not hibernate, True)
