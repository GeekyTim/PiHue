#!/usr/bin/python3

'''
    File name: PiHueLightList.py
    Author: Tim Richardson
    Date created: 04/07/2017
    Date last modified: 10/07/2017
    Python Version: 3.4

	Description:
	Control Philips Hue lights using a Pimoroni TouchpHAT - individual light version

    Requirements:
    * Raspberry Pi (http://raspberrypi.org/)
    * Philips Hue (http://www2.meethue.com)
    * Pimoroni TouchpHAT (https://shop.pimoroni.com/products/touch-phat)

    The Raspberry Pi must be on the same network as the Hue bridge
    You must set the bridgeip to be the IP address of your bridge
    and edit the list of lights in your network in 'lights[]'

    You can edit/expand the colour 'xy' values and the alerts
'''

# Import libraries
# Install phue and touchphat with pip3
# pip3 install phue
# pip3 install touchphat
from phue import Bridge
import touchphat
import time

# ==============================================================================================
# Setup
# ==============================================================================================
touchphat.all_off()

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Stuff you need to change!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# The IP address of the Hue bridge and a list of lights you want to use
bridgeip = '192.168.13.178'  # <<<<<<<<<<<
lights = ['Desk', 'Ikea']  # <<<<<<<<<<<

# -----------------------------------------------------------------------------------------------
# Do some internal setup
# -----------------------------------------------------------------------------------------------
# Connect to the bridge
b = Bridge(bridgeip)

# IMPORTANT: If running for the first time:
#    Uncomment the b.connect() line
#    Ppress button on bridge
#    Run the code
# This will save your connection details in /home/pi/.python_hue
# Delete that file if you change bridges
# b.connect() # <<<<<<<<<<

# An array of the light name and the light type.
# Expand if you have something different - please let me know if you do!
lighttype = []
lighttypecolour = 'Extended color light'
lighttypedimmable = 'Dimmable light'
# Get the type of lights that are connected
for light in lights:
    lighttype.append([light, b.get_light(light, 'type')])

# Hue 'xy' colours - expand at will
redxy = (0.675, 0.322)
greenxy = (0.4091, 0.518)
bluexy = (0.167, 0.04)
yellowxy = (0.4325035269415173, 0.5007488105282536)
bluevioletxy = (0.2451169740627056, 0.09787810393609737)
orangexy = (0.6007303214398861, 0.3767456073628519)
whitexy = (0.32272672086556803, 0.3290229095590793)

# Alert Patterns
# Used to change the status of lights
# First two numbers are the number of repeat cycles, and the delay between changes
# Followed by dictionaries of the change of light status.
# Use any valid HUE setting - e.g. on, bri, xy, ct, sat, hue, transformationtime
redAlert = [6, 0.5,
            {lighttypecolour: {'on': True, 'bri': 255, 'xy': redxy, 'transitiontime': 0},
             lighttypedimmable: {'on': True, 'bri': 255, 'transitiontime': 0}},
            {lighttypecolour: {'on': False, 'bri': 255, 'xy': redxy, 'transitiontime': 0},
             lighttypedimmable: {'on': False, 'bri': 255, 'transitiontime': 0}}]

amberAlert = [6, 0.5,
              {lighttypecolour: {'on': True, 'bri': 255, 'xy': orangexy, 'transitiontime': 0},
               lighttypedimmable: {'on': True, 'bri': 255, 'transitiontime': 0}},
              {lighttypecolour: {'on': False, 'bri': 255, 'xy': orangexy, 'transitiontime': 0},
               lighttypedimmable: {'on': False, 'bri': 255, 'transitiontime': 0}}]

blueAlert = [6, 0.5,
             {lighttypecolour: {'on': True, 'bri': 255, 'xy': bluexy, 'transitiontime': 0},
              lighttypedimmable: {'on': True, 'bri': 255, 'transitiontime': 0}},
             {lighttypecolour: {'on': False, 'bri': 255, 'xy': bluexy, 'transitiontime': 0},
              lighttypedimmable: {'on': False, 'bri': 255, 'transitiontime': 0}}]

greenAlert = [6, 0.5,
              {lighttypecolour: {'on': True, 'bri': 255, 'xy': greenxy, 'transitiontime': 0},
               lighttypedimmable: {'on': True, 'bri': 255, 'transitiontime': 0}},
              {lighttypecolour: {'on': False, 'bri': 255, 'xy': greenxy, 'transitiontime': 0},
               lighttypedimmable: {'on': False, 'bri': 10, 'transitiontime': 0}}]

allwhite = {lighttypecolour: {'on': True, 'bri': 255, 'xy': whitexy, 'transitiontime': 4},
            lighttypedimmable: {'on': True, 'bri': 255, 'transitiontime': 4}}

# If an alert is ongoing, this will be True
inalert = False

# Wait time between sending messages to the bridge - to stop congestion
defaultwaittime = 0.41


# = End of Setup ============================================================================

# -------------------------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------------------------

# Get the status of every light in the list of lights
# Extend this if there are more light types in your network
# Return Value: Dictionary of the status of all lights in the list
def getlightstatus():
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


# Return the status of the lights to what they were before the alert
# Input: Dictionary of the status of all lights in the list (obtained from getlightstatus()
def putlightstatus(lightstatus):
    global lights

    for light in lights:
        b.set_light(light, lightstatus[light])
        time.sleep(defaultwaittime)


# Runs through the alert dictionary defined in alertpattern
# Input: alertpattern containes the pre-defined alert pattern
def huealert(alertpattern):
    global inalert, lighttype

    # Only run if we're not already in an alert
    if not inalert:
        inalert = True
        # Get the current status of the lamps
        preAlertStatus = getlightstatus()

        # Using the pre-defined alert patterns, change the lamp status
        for rep in range(alertpattern[0]):
            for runalert in range(2, len(alertpattern)):
                for light in lighttype:
                    b.set_light(light[0], alertpattern[runalert][light[1]])
                    time.sleep(alertpattern[1])

        # Return the lamps to the previous status
        putlightstatus(preAlertStatus)
        inalert = False


# Identifies if any of the lamps in the list are on
# Return Value: True if any lamps are on, otherwise False
def islampon():
    global inalert

    result = False

    if not inalert:
        islighton = getlightstatus()
        for light in lights:
            if islighton[light]['on']:
                result = True

    return result


# When the A button is pressed, run redalert
@touchphat.on_touch("A")
def toucha():
    huealert(redAlert)
    touchphat.led_off("A")


# When the B button is pressed, run amberAlert
@touchphat.on_touch("B")
def touchb():
    huealert(amberAlert)
    touchphat.led_off("B")


# When the C button is pressed, run greenAlert
@touchphat.on_touch("C")
def touchc():
    huealert(greenAlert)
    touchphat.led_off("C")


# When the D button is pressed, run blueAlert
@touchphat.on_touch("D")
def touchd():
    huealert(blueAlert)
    touchphat.led_off("D")


# When 'enter' is pressed, all lights are turned on to 'bright white'
# (i.e. what is defined in the dictionary 'allwhite'. Change at will.
@touchphat.on_touch("Enter")
def touchenter():
    global lighttype

    for light in lighttype:
        b.set_light(light[0], allwhite[light[1]])
        time.sleep(defaultwaittime)
    touchphat.led_off("Enter")
    touchphat.led_on("Back")


# When the Back button is pressed, toggle the lamp on/off status
@touchphat.on_touch("Back")
def touchback():
    global inalert

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


# ================================================================
# Main loop - keep going forever
# ================================================================
while True:
    if inalert:
        time.sleep(1)
    else:
        if islampon():
            touchphat.led_on("Back")
        else:
            touchphat.led_off("Back")
        time.sleep(10)
