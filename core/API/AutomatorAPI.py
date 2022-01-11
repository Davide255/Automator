import asyncio, sys
if sys.version_info >= (3, 8, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class AutomatorAPI():
    '''
    AUTOMATOR API
    =============
    The Automator Api is an experimental function that allow you to use automator as a library to interact with system and creating
    temporary automations.'''
    
    class Battery:
        def get_battery_info(self):
            from winrt.windows.system.power import PowerManager
            return {'level':PowerManager.get_remaining_charge_percent(), 'charging':True if PowerManager.get_battery_status() == 3 else False}

    class Bluetooth:

        async def _set_state(self, state):
            from winrt.windows.devices.radios import Radio
            
            info = await Radio.get_radios_async()
            bluetooth = info.first().current

            await bluetooth.set_state_async(state)
            return True

        def set_on(self):
            from winrt.windows.devices.radios import RadioState
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            loop.run_until_complete(self._set_state(RadioState.ON))
            loop.close()
            return True

        def set_off(self):
            from winrt.windows.devices.radios import RadioState
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            loop.run_until_complete(self._set_state(RadioState.OFF))
            loop.close()
            return True
    
    class Network:
        def enum_aviable_networks(self):
            import logging
            from libs.Win32Wifi import WlanOpenHandle, WlanEnumInterfaces, WlanCloseHandle, WlanScan, WlanGetAvailableNetworkList

            handle = WlanOpenHandle()
            interfaces = WlanEnumInterfaces(handle).contents
            g = interfaces.InterfaceInfo[0].InterfaceGuid
            WlanScan(handle, g)
            networks= WlanGetAvailableNetworkList(handle, g).contents
            logging.debug("Number of networks found : ", networks.NumberOfItems)
            network_ssids = list()
            for i in range(networks.NumberOfItems):
                network_ssids.append(networks.Network[i].dot11Ssid.SSID)
            WlanCloseHandle(handle)

            return network_ssids

        def connect(self, parms):
            network = parms

            from libs.Win32Wifi import WlanOpenHandle, WlanEnumInterfaces, WlanCloseHandle, WlanConnect, \
            WLAN_CONNECTION_PARAMETERS, LPCWSTR, DOT11_SSID

            ssid = DOT11_SSID()
            ssid.SSID = network.encode('utf-8')
            ssid.SSIDLength = len(list(network))

            parms = WLAN_CONNECTION_PARAMETERS()
            parms.wlanConnectionMode = 0
            parms.strProfile = LPCWSTR(network)
            parms.pDot11Ssid = ssid
            parms.pDesiredBssidList = None
            parms.dot11BssType = 3
            parms.dwFlags = 0

            handle = WlanOpenHandle()
            interfaces = WlanEnumInterfaces(handle).contents
            g = interfaces.InterfaceInfo[0].InterfaceGuid
            WlanConnect(handle, g, parms)
            WlanCloseHandle(handle)
            return True

        def disconnect(self):
            from libs.Win32Wifi import WlanOpenHandle, WlanEnumInterfaces, WlanCloseHandle, WlanDisconnect
            handle = WlanOpenHandle()
            interfaces = WlanEnumInterfaces(handle).contents
            g = interfaces.InterfaceInfo[0].InterfaceGuid
            WlanDisconnect(handle, g)
            WlanCloseHandle(handle)

    class Process:
        def is_running(self, pid=None, name=None):
            if pid != None:
                import wmi
                c = wmi.WMI ()
                for process in c.Win32_Process ():
                    if pid == process.ProcessId:
                        return True
                return False
            elif name != None:
                import ctypes.wintypes, os

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
                                return True
                        CloseHandle(hProcess)
                return False
            else:
                return False