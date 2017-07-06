#!/usr/bin/python3

# Import libraries
# Install phue and touchphat with pip3
# pip3 install phue
# pip3 install touchphat
from phue import Bridge
import touchphat
import os.path
import time
from rgbxy import Converter

# Setup
touchphat.all_off()

bridgeip = '192.168.13.180'
lights = ['Test lamp']

b = Bridge(bridgeip)

# If running for the first time, press button on bridge and run with b.connect() uncommented
if (os.path.exists("/home/pi/.python_hue") == False):
    print('Press the Hue`s connect button')
    b.connect()

# Alert Patterns - used to change the status of lights
# First do some RGB to XY conversion
converter = Converter()
redxy = converter.rgb_to_xy(255, 0, 0)
greenxy = converter.rgb_to_xy(0, 255, 0)
bluexy = converter.rgb_to_xy(0, 0, 255)
yellowxy = converter.rgb_to_xy(255, 255, 0)
bluevioletxy = converter.rgb_to_xy(138, 43, 226)
orangexy = converter.rgb_to_xy(255, 140, 0)

redAlert = [3,
            {'transitiontime': 10, 'on': True, 'bri': 254, 'xy': redxy},
            {'transitiontime': 10, 'on': True, 'bri': 254, 'xy': bluexy}]

soonAlert = [3,
             {'transitiontime': 15, 'on': True, 'bri': 254, 'xy': greenxy},
             {'transitiontime': 15, 'on': True, 'bri': 254, 'xy': bluevioletxy}]

phoneAlert = [6,
              {'transitiontime': 5, 'on': True, 'bri': 254, 'xy': orangexy},
              {'transitiontime': 5, 'on': True, 'bri': 254, 'xy': yellowxy}]

# If an alert is ongoing, thjis will be True
inalert = False

# -------------------------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------------------------

# Get the status of every light in the list of lights
def getlightstatus():
    lightStatus = []
    for light in lights:
        lightStatus.append({'transitiontime': 20,
                            'on': b.get_light(light, 'on'),
                            'bri': b.get_light(light, 'bri'),
                            'xy': b.get_light(light, 'xy')})
    return lightStatus


def putlightstatus(lightstatus):
    for light in range(len(lights)):
        b.set_light(lights[light], lightstatus[light])
    time.sleep(2.1)


def huealert(alertpattern):
    global inalert

    inalert = True
    # Get the current status of the lamps
    preAlertStatus = getlightstatus()

    # Using the pre-defined alert patterns, change the lamp status
    for rep in range(alertpattern[0]):
        for runalert in range(1, len(alertpattern)):
            b.set_light(lights, alertpattern[runalert])
            time.sleep(alertpattern[runalert]['transitiontime'] / 10.0)

    # Return the lamps to the previous status
    putlightstatus(preAlertStatus)
    inalert = False

def islampon():
    global inalert

    result = False

    if not inalert:
        islighton = getlightstatus()
        for light in range(len(lights)):
            if islighton[light]['on']:
                result = True

    return result

# When the A button is pressed, run redalert
@touchphat.on_touch("A")
def toucha():
    huealert(redAlert)
    touchphat.led_off("A")

# When the B button is pressed, run soonAlert
@touchphat.on_touch("B")
def toucha():
    huealert(soonAlert)
    touchphat.led_off("B")

# When the D button is pressed, run phoneAlert
@touchphat.on_touch("D")
def toucha():
    huealert(phoneAlert)
    touchphat.led_off("D")

# When the Back button is pressed, toggle the lamp status
@touchphat.on_touch("Back")
def touchback():
    if not inalert:
        if islampon():
            touchphat.led_off("Back")
            for light in lights:
                b.set_light(light, 'on', False)
        else:
            touchphat.led_on("Back")
            for light in lights:
                b.set_light(light, 'on', True)

while True:
    if inalert:
        time.sleep(1)
    else:
        if islampon():
            touchphat.led_on("Back")
        else:
            touchphat.led_off("Back")
        time.sleep(10)
