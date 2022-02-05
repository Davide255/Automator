# WELCOME TO AUTOMATOR BETA 

### This program is able to create automations on your system.
### WARNING: this program is only an experimantal release; infact it works very well on Windows wether in linux did not works always correctly

### Aviable languages:
  * Italian
  * English

### Tested with these systems: 
  * Windows 10 (build 19043.1237)
  * Windows 11 (build 22000)

# Updates

- Fixed Network bug using windows API
- Adding .exe support and create first pakage
- Updated Process calsses in execute file
- Fixed general bug
   
# Installation
 - # Prerequisites

   - Python 3.6 =< =>3.9 (CURRENT NOT SUPPORTED PYHON 3.10), pip pakage manager 
   - !! WINDOWS SYSTEM ONLY !!

 - ## Installation
    
    - Downolad and extract this pakage.
     
    - Install the pakage dipendency by pip: 
     
      <code>pip install -r requirements_win32.txt</code>

    - If you have installed Visual Studio or VSCode you can copy this repository
      and follow the above steps.

# How does it works?

The main programm create a Thread that observe your system and it does actions consequentially.

# How to create Automations on this BETA?

To crate a new automation, you can add at the 'Automator.json' a new dict like that:
```json
     [               
          {}
     ]
 ```
 define a title:
 ```json
     "title" : "My Awesome Automation",
 ```                
 define an optional subtitle:
 ```json     
     "subtitle" : "My Really Awesome Automation",
 ```                 
 define if the automation will be active or not:
 ```json     
      "active": true,
 ```                
 define an empty dict with key "added_prpriety"
 ```json     
      "added_propriety": {},
 ```                
 define the actions dict that tells Automator what to do
 ```json
      "actions": {
 ```
 define the actions dict this will be the event that will activate your automation
 
 ## Actions API
 
      parameter_name: usage --> explanetion

 Battery:
 
      level: "Battery", "level", "x" --> if battery is on x% 
      plugged or not_plugged: "Battery", "plugged"/"not_plugged" --> if battery is plugged or not
      
 Network:
 
      is_connected: "Network", "is_connected", "wifi_ssid" --> if your machine is connected to wifi_ssid
      
 Process:
      
      is_running: "Process", "is_running", "method", "process_name" --> method should be "pid", "x = process pid"
                                                                        or "name", "x = executable_name.exe"
                                                                        
 System:
 
      on_brightness: "Sysyem", "on_brightness", "x" --> if screen brightness is "x"
      
 Startup:
 
      takes no parameters --> At the startup of Automator

 ## Simple example:
  
      "automation": [ ["Battery", "level", "100"] ]      
     or: 
      "automation": [ ["Process", "is_running", "name", "chrome.exe"] ]
                                                             ^
                             (writing "chrome" will work but we recommend to add the extension)
                             
  now define the actions that your system will do on automation event:
  
  ## Actions API
  
  Network: 
      
      connect: "Network", "connect", wifi_ssid --> if isn't wifi_ssid this will do noathing
      disconnect: "Network", "disconnect" --> this will take no parameters and it will disconnect from current wifi
  
  Bluetooth:
  
      set_on: "Bluetooth", "switch_on"/"switch_off" --> switch on/off the bluetooth sensor
      
  Process:
  
      start: "Process", "start", "filename.ext" --> start filename.ext, YOU MUST INSERT THE EXTENSION
      kill: "Process", "kill", "process.exe" --> Kills all process called "process.exe"
      
  Audio:
  
      set_master_volume_level: "Audio", "set_master_volume_level", "x" --> sets the master_volume to x% (do not insert %)
      mute_process: "Audio", "mute_process", "process_name" --> mute all process called process_name 
                                                                (can contain the extension but isn't required)
      unmute_process: "Audio", "unmute_process", "process_name" --> mute all process called process_name 
                                                                    (can contain the extension but isn't required)
      stop/play_audio: "Audio", "stop/play_audio" --> virtual press the stop media button (0xB3)
      play_audio: "Audio", "play_audio", "audio_name.mp3", "Optional Stoppable" --> play an MP3 file, if Optional Stoppable
                                                                                    is True the audio will be stoppable with 
                                                                                    0xB3 key else only by the menu
      
  System:
  
      reboot: "System", "reboot" --> reboot the system
      shotdown: "System", "shotdown" --> shotdown the system
      suspend: "System", "suspend"/"hibernate" --> set suspend/hiberante state
      look: "System", "look" --> look the system displaying the login screen
      logoff: "System", "logoff" --> terminate the current Windows session and return ath the login screen
      set_brightness: "System", "set_brightness", "x" --> set the brigthness to x%
      take_screenshot: "System", "take_screenshot", "screenshot_name.ext" --> take a screenshot and save it as screenshot_name.ext
                                                                              (RACCOMANDED: specify the file extension)
      send_notification: "System", "send_notification", {"title": "Awesome Notification", --> the title of the notification
                                                         "msg": "My awesome and beautifull notification"} --> the notification
                                                                                                             corpus
                                                                                                             
  ## Simple example:      
   
      "action_to_do": [ ["System", "reboot"] ]
      or
      "action_to_do": [ ["System", "take_screenshot", "screenshot.png"] ]
      
      
  Now your dict should be like this:
  
  ```json
       [  
       
          {
                "title" : "My Awesome Automation",
                "subtitle" : "My Really Awesome Automation",
                "active": true,
                "added_propriety": {},
                "actions": {
                     "automation": [ ["your actions"] ],
                     "action_to_do": [ ["your actions"] ]
                     }
           },
           
           { "Other Automation": {}
           },
       ]
 ```
 
 Now save and restart Automator
 
 On the main UI you should see somethink like this:
 ![Screenshot (12)](https://user-images.githubusercontent.com/80689057/139920483-9212f264-6351-437e-a2ca-37253b2b59ba.png)
 
# Author
Davide Berardi

# Version
0.13 BETA dev
