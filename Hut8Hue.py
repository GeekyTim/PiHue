#!/usr/bin/python3

# Import libraries
# Install phue and touchphat with pip3
# pip3 install phue
# pip3 install touchphat
from phue import Bridge
import touchphat
import os.path
import time

#==============================================================================================
# Setup
touchphat.all_off()

# The IP address of the Hue bridge and a list of lights you want to use
bridgeip = '192.168.13.178'
lights = ['Desk', 'Ikea']

b = Bridge(bridgeip)

# If running for the first time, press button on bridge and run with b.connect() uncommented
#b.connect()

lighttype = []
lighttypecolour = 'Extended color light'
lighttypedimmable = 'Dimmable light'
# Get the type of lights that are connected
for light in lights:
    lighttype.append([light, b.get_light(light, 'type')])

# Alert Patterns - used to change the status of lights
# Colours - expand at will
redxy       = (0.675, 0.322)
greenxy     = (0.4091, 0.518)
bluexy      = (0.167, 0.04)
yellowxy    = (0.4325035269415173, 0.5007488105282536)
bluevioletxy= (0.2451169740627056, 0.09787810393609737)
orangexy    = (0.6007303214398861, 0.3767456073628519)
whitexy     = (0.32272672086556803, 0.3290229095590793)

# Four different alerts
# First two numbers are the number of repeat cycles, and the delay between changes
# Followed by dictionaries of the change of light status.
# Use any valid HUE setting - e.g. on, bri, xy, ct, sat, hue, transformationtime
redAlert = [5, 0.5,
            {lighttypecolour: {'on': True, 'bri': 254, 'xy': redxy},
             lighttypedimmable: {'on': True, 'bri': 255}},
            {lighttypecolour: {'on': True, 'bri': 254, 'xy': bluexy},
             lighttypedimmable: {'on': True, 'bri': 10}}]

soonAlert = [3, 1,
            {lighttypecolour: {'on': True, 'bri': 254, 'xy': greenxy},
             lighttypedimmable: {'on': True, 'bri': 255}},
            {lighttypecolour: {'on': True, 'bri': 254, 'xy': bluevioletxy},
             lighttypedimmable: {'on': True, 'bri': 10}}]

phoneAlert = [6, 0.5,
            {lighttypecolour: {'on': True, 'bri': 254, 'xy': orangexy},
             lighttypedimmable: {'on': True, 'bri': 255}},
            {lighttypecolour: {'on': True, 'bri': 254, 'xy': yellowxy},
             lighttypedimmable: {'on': True, 'bri': 10}},
            {lighttypecolour: {'on': True, 'bri': 254, 'xy': bluexy},
             lighttypedimmable: {'on': True, 'bri': 10}}]

foodAlert = [6, 0.5,
            {lighttypecolour: {'on': True, 'bri': 254, 'xy': whitexy},
             lighttypedimmable: {'on': True, 'bri': 255}},
            {lighttypecolour: {'on': True, 'bri': 254, 'xy': whitexy},
             lighttypedimmable: {'on': True, 'bri': 10}}]

allwhite = [1, 0.5,
            {lighttypecolour: {'on': True, 'bri': 254, 'xy': whitexy},
             lighttypedimmable: {'on': True, 'bri': 255}}]
# If an alert is ongoing, this will be True
inalert = False
#==============================================================================================

# -------------------------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------------------------

# Get the status of every light in the list of lights
# Extend this if there are more light types in your network
def getlightstatus():
    print('getlightstatus')
    lightStatus = {}
    for light in lights:
        lighttype = b.get_light(light, 'type')
        if lighttype == lighttypecolour:
            lightStatus.update({light: {'on': b.get_light(light, 'on'),
                                'bri': b.get_light(light, 'bri'),
                                'xy': b.get_light(light, 'xy')}})
        elif lighttype == lighttypedimmable:
            lightStatus.update({light: {'on': b.get_light(light, 'on'),
                                'bri': b.get_light(light, 'bri')}})

    return lightStatus


def putlightstatus(lightstatus):
    print('putlightstatus')
    for light in range(len(lights)):
        b.set_light(lights[light], lightstatus[light])

def huealert(alertpattern):
    global inalert

    print('huealert')

    if not inalert:
        inalert = True
        # Get the current status of the lamps
        preAlertStatus = getlightstatus()
        print(preAlertStatus)

        # Using the pre-defined alert patterns, change the lamp status
        for rep in range(alertpattern[0]):
            for runalert in range(2, len(alertpattern)):
                b.set_light(lights, alertpattern[runalert])
                time.sleep(alertpattern[1])

        # Return the lamps to the previous status
        putlightstatus(preAlertStatus)
        inalert = False

def islampon():
    global inalert
    print('islampon')

    result = False

    if not inalert:
        islighton = getlightstatus()
        print (islighton)
        for light in lights:
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

# When the C button is pressed, run soonAlert
@touchphat.on_touch("C")
def toucha():
    huealert(foodAlert)
    touchphat.led_off("C")

# When the D button is pressed, run phoneAlert
@touchphat.on_touch("D")
def toucha():
    huealert(phoneAlert)
    touchphat.led_off("D")

# When enter is pressed, all lights are turned on to bright white
@touchphat.on_touch("Enter")
def touchenter():
    for light in lights:
        b.set_light(light, 'on', True)
        b.set_light(light, 'xy', whitexy) # This will cause an handled error on lamps that don't have the xy values
        b.set_light(light, 'bri', 255)
    touchphat.led_off("Enter")
    touchphat.led_on("Back")

# When the Back button is pressed, toggle the lamp on/off status
@touchphat.on_touch("Back")
def touchback():
    global inalert

    print('touchback')
    if not inalert:
        lampon = islampon()
        inalert = True
        if lampon:
            for light in lights:
                b.set_light(light, 'on', False)
            touchphat.led_off("Back")
        else:
            for light in lights:
                b.set_light(light, 'on', True)
            touchphat.led_on("Back")
        time.sleep(1)
        inalert = False

#================================================================
# Main loop - keep going forever
#================================================================
while True:
    if inalert:
        print('inalert')
        time.sleep(1)
    else:
        print('not inalert')
        if islampon():
            touchphat.led_on("Back")
        else:
            touchphat.led_off("Back")
        time.sleep(10)
