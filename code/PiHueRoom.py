#!/usr/bin/python3

"""
File name: PiHueRoom.py
Author: Tim Richardson
Date created: 04/07/2017
Date last modified: 14/08/2021
Python Version: 3.4

Description:
Control Philips Hue lights using a Pimoroni TouchpHAT - Room version

Requirements:
* Raspberry Pi (http://raspberrypi.org/)
* Philips Hue (http://www2.meethue.com)
* Pimoroni Touch pHAT (https://shop.pimoroni.com/products/touch-phat)

The Raspberry Pi must be on the same network as the Hue bridge
You must set the bridge to be the IP address of your bridge
and edit the room constant 'roomname'

You can edit/expand the colour 'xy' values and the alerts

Import libraries
Install phue and touchphat with pip3:
    sudo apt install python3-cap1xxx python3-pip  python3-touchphat
    sudo pip3 install phue
"""

from signal import pause

import touchphat

import colourconfig
import hueconfig
import huecontrol

# ==============================================================================================
# Setup
# ==============================================================================================
touchphat.all_off()


# -------------------------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------------------------
# When the A button is pressed, run redalert
@touchphat.on_touch("A")
def toucha():
    huelights.alert(colourconfig.alert_red)
    touchphat.led_off("A")


# When the B button is pressed, run alert_amber
@touchphat.on_touch("B")
def touchb():
    huelights.alert(colourconfig.alert_amber)
    touchphat.led_off("B")


# When the C button is pressed, run alert_green
@touchphat.on_touch("C")
def touchc():
    huelights.alert(colourconfig.alert_green)
    touchphat.led_off("C")


# When the D button is pressed, run alert_blue
@touchphat.on_touch("D")
def touchd():
    huelights.alert(colourconfig.alert_blue)
    touchphat.led_off("D")


# When 'enter' is pressed, the room is turned on to 'bright white'
# (i.e. what is defined in the dictionary 'allwhite'. Change at will.
@touchphat.on_touch("Enter")
def touchenter():
    huelights.setcolour(colourconfig.allwhite)
    touchphat.led_on("Enter")
    touchphat.led_off("Back")


# When the Back button is pressed, toggle the lamp on/off status
@touchphat.on_touch("Back")
def touchback():
    huelights.turnoff()
    touchphat.led_off("Back")
    touchphat.led_off("Enter")


# ================================================================
# Main loop - keep going forever
# ================================================================
def main():
    pause()


if __name__ == "__main__":
    huelights = huecontrol.HueControl(hueconfig.bridge, hueconfig.roomname, hueconfig.waittime)
    main()
