import sys
import psutil

def get_battery_info():
    if sys.platform == 'linux':
        try:
            charge_state = open("/sys/class/power_supply/BAT1/status","r").readline().strip()
        except FileNotFoundError:
            try:
                charge_state = open("/sys/class/power_supply/BAT0/status","r").readline().strip()
            except FileNotFoundError:
                charge_state = None
        
        try:
            capacity = open("/sys/class/power_supply/BAT1/capacity","r").readline().strip()
        except FileNotFoundError:
            try:
                capacity = open("/sys/class/power_supply/BAT0/capacity","r").readline().strip()
            except FileNotFoundError:
                capacity = None
        
        return[capacity, charge_state]

    else:
        from winrt.windows.system.power import PowerManager
        return [PowerManager.get_remaining_charge_percent(), True if PowerManager.get_battery_status() == 3 else False]