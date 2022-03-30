def enum_aviable_networks():
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

def connect(network):
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

def disconnect():
    from libs.Win32Wifi import WlanOpenHandle, WlanEnumInterfaces, WlanCloseHandle, WlanDisconnect
    handle = WlanOpenHandle()
    interfaces = WlanEnumInterfaces(handle).contents
    g = interfaces.InterfaceInfo[0].InterfaceGuid
    WlanDisconnect(handle, g)
    WlanCloseHandle(handle)