# PiHue
Controlling Philips Hue with a Pimoroni Touch pHAT

## Introduction
The purpose of this code is to control Philips Hue lights using a Raspberry Pi and Pimoroni Touch pHAT. Each button on the Touch pHAT can have a different function.  In this case I have decided on the following:
* The 'Return' button will toggle the lights on and off. The LED indicator will show you whether any lights in the room/list are on.
* The 'Enter' button will turn all the lights in the room or list to bright.
* Button 'A' will flash the lights red
* Button 'B' will flash the lights amber
* Button 'C' will flash the lights green
* Button 'D' will flash the lights blue

The intended use is for the Touch pHAT to be placed in one room and the lights in another (or in my case, Hut 8) alert me to a situation (e.g. dinner is ready, she is home, phone call etc).  I can also turn off the lights remotely without using the Hue app or Alexa.

## Hardware Requirements
* [Raspberry Pi](http://raspberrypi.org/)
    * SD card with Raspbian Jessie installed (preferably Raspbian Lite)
    * Connected to the same network as the Philips Hue
* [Philips Hue](http://www2.meethue.com)
    * You need to know the IP address of your Hue bridge.
* [Pimoroni Touch pHAT](https://shop.pimoroni.com/products/touch-phat)

## Prerequisites
Some prerequisites need to be installed for this code:
* Python 3, PIP and GIT

    ```text
    sudo apt-get update
    sudo apt-get install python3 python3-pip git
* The Pimoroni Touch pHAT library
    ```text
    apt-get install python3-touchphat

* The 'phue' Python Hue library from [StudioImagineaire](http://studioimaginaire.com/en/projects/phue/), and available on [GitHub](https://github.com/studioimaginaire/phue)
    ```text
    sudo pip3 install phue

## Cloning from GitHub
The best way to get this code is to clone it from GitHub with:

    git clone https://github.com/GeekyTim/PiHue
    
The PiHue code will be in the directory ``PiHue``

    cd PiHue

## Set Up
There are two versions of the code:
* One that controls a room of lights (i.e. a Room): PiHueRoom.py
* Another that controls individual lights: PiHueLightList.py

Choose which version you prefer. I find that the Room version works best with one room that contains both a dimable light and a colour light.

Edit the code to make the following **REQUIRED** changes:
* For PiHueRoom.py:
    * Change the IP address of your Philips Hue: ``bridgeip``
    * Change the name of the room you want to control: ``roomname``
* For PiHueLightList.py:
    * Change the IP address of your Philips Hue: ``bridgeip``
    * Change the names of the lights you want to control in the Python list: ``lights``

Optionally you can change the list of 'xy' colours by adding/altering/replacing to those already listed under ```# Hue 'xy' colours - expand at will```
You can change the 'alert' patterns in the section following ``# Alert Patterns``. These are Python lists:
* The first two numbers are the number of repeat cycles, and the delay between light changes. Recommended minimum delay between changes is 0.4s.
* The remaining values are Python dictionaries of the light status changes.
    * Use any valid Hue status, e.g. 'on', 'bri', 'xy', 'ct', 'sat', 'hue', 'transformationtime'.
    * Remember that Dimable Lights do not accept any of the colour changes (i.e. 'xy', 'ct', 'sat', 'hue'), so you will need to change their brightness.
    * You can have as many changes as you need.
    * For Roomss, if you have dimmable lights as well as colour lights, you should alter the brightness as well as the colour of the rooms' lights.
    * For Light Lists the status changes are themselves Python dictionaries that contain the changes for each light type (e.g. 'Extended color light'
and 'Dimmable light'). If you have different light types, you can add them to the dictionary.
* There is one special dictionary that is used by the 'enter' key to set all lights to on and maximum white: ``allwhite``. You can redefine this to be any colour and brightness that you prefer.

## Running the Code for the First Time
The first time you run the code, you **MUST** first uncomment the line ``# b.connect()`` and press your Bridge connect button just before running the code with either:

    python3 PiHueRoom.py

or

    python3 PiHueLightList.py

Your Pi should connect to the Bridge and save the Bridge details and user in the file ``/home/pi/.python_hue``

If you ever need to change your Bridge details, just delete this file.

You can now recomment the ``b.connect()`` line.

## Running on Boot
There are a few ways to run Python code on booting your Raspberry Pi. My preferred method is to use Systemd.

### Create A 'Unit File'
Create a configuration file (aka a unit file) that tells systemd what we want it to do and when:

    sudo nano /lib/systemd/system/PiHue.service

Add in the following text (replacing PiHueRoom.py with PiHueLightList.py as required):

    [Unit]
    Description=PiHue Service
    After=multi-user.target
    
    [Service]
    Type=idle
    User=pi
    Restart=always
    RestartSec=5
    ExecStart=/usr/bin/python3 /home/pi/PiHue/PiHueRoom.py
    
    [Install]
    WantedBy=multi-user.target

Save and exit the nano editor using [CTRL-X], [Y] then [ENTER].

This defines a new service called “PiHue Service”.

The permission on the unit file needs to be set to 644 :

    sudo chmod 644 /lib/systemd/system/PiHue.service

### Configure systemd

Instruct systemd to start the service during the boot sequence:

    sudo systemctl daemon-reload
    sudo systemctl enable PiHue.service

Reboot the Pi and the PiHue service should run:

    sudo reboot

### Check the Status of the PiHue service

You can check the status of your service using:

    sudo systemctl status PiHue.service

This should return something looking like:


    PiHue.service - Start the TouchpHAT Hue controller
       Loaded: loaded (/lib/systemd/system/PiHue.service; enabled)
       Active: active (running) since Mon 2017-07-10 23:26:52 UTC; 15min ago
     Main PID: 746 (python3)
       CGroup: /system.slice/PiHue.service
               └─746 /usr/bin/python3 /home/pi/PiHue/PiHueRoom.py
    
    Jul 10 23:26:52 PiHue systemd[1]: Starting Start the TouchpHAT Hue controller...
    Jul 10 23:26:52 PiHue systemd[1]: Started Start the TouchpHAT Hue controller.

## Rebooting your Raspberry Pi on Network Loss

You may find that your Raspberry Pi occasionally disconnects from your network, especially if you are using Wifi.  Once disconnected, unless you do restart the network interface or reboot the Pi, it will remain disconnected.

If this is happening then you may want to use this little service to reboot your Pi, but be careful, if you move the IP address you set becomes unavailable (e.g. if you use your Pi away from home) then it may keep rebooting itself ad infinitum!

Follow the instructions by Thijs Bernolet on his [blog](http://weworkweplay.com/play/rebooting-the-raspberry-pi-when-it-loses-wireless-connection-wifi/) to enable reboot on network loss.


## Suggestions
This code is only an example of what I want to use the TouchpHAT to do. There is plenty more - like having each button turn on a different light in the house, or connecting a motion or temperature sensor to change light colour - feel free to take this code and modify at will, but PLEASE attribute both the 'phue' [library developer](https://github.com/studioimaginaire/phue) and myself as is customary.

Please feel free to tweet me [@Geeky_Tim](https://twitter.com/Geeky_Tim)
