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
    You must set the bridge to be the IP address of your bridge
    and edit the list of lights in your network in 'lights[]'

    You can edit/expand the colour 'xy' values and the alerts
'''

import time

import touchphat
# Import libraries
# Install phue and touchphat with pip3
# pip3 install phue
# pip3 install touchphat
from phue import Bridge

# ==============================================================================================
# Setup
# ==============================================================================================
touchphat.all_off()

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Stuff you need to change!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# The IP address of the Hue bridge and a list of lights you want to use
bridgeip = 'StarFleet-Hue.localdomain' #'192.168.13.178'  # <<<<<<<<<<<
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
red = (0.675, 0.322)
green = (0.4091, 0.518)
blue = (0.167, 0.04)
yellow = (0.4325035269415173, 0.5007488105282536)
blueviolet = (0.2451169740627056, 0.09787810393609737)
orange = (0.6007303214398861, 0.3767456073628519)
white = (0.32272672086556803, 0.3290229095590793)

# Alert Patterns
# Used to change the status of lights
# First two numbers are the number of repeat cycles, and the delay between changes
# Followed by dictionaries of the change of light status.
# Use any valid HUE setting - e.g. on, bri, xy, ct, sat, hue, transformationtime
alert_red = [6, 0.5,
             {lighttypecolour  : {'on': True, 'bri': 255, 'xy': red, 'transitiontime': 0},
             lighttypedimmable: {'on': True, 'bri': 255, 'transitiontime': 0}},
             {lighttypecolour  : {'on': False, 'bri': 255, 'xy': red, 'transitiontime': 0},
             lighttypedimmable: {'on': False, 'bri': 255, 'transitiontime': 0}}]

alert_amber = [6, 0.5,
               {lighttypecolour  : {'on': True, 'bri': 255, 'xy': orange, 'transitiontime': 0},
               lighttypedimmable: {'on': True, 'bri': 255, 'transitiontime': 0}},
               {lighttypecolour  : {'on': False, 'bri': 255, 'xy': orange, 'transitiontime': 0},
               lighttypedimmable: {'on': False, 'bri': 255, 'transitiontime': 0}}]

alert_blue = [6, 0.5,
              {lighttypecolour  : {'on': True, 'bri': 255, 'xy': blue, 'transitiontime': 0},
              lighttypedimmable: {'on': True, 'bri': 255, 'transitiontime': 0}},
              {lighttypecolour  : {'on': False, 'bri': 255, 'xy': blue, 'transitiontime': 0},
              lighttypedimmable: {'on': False, 'bri': 255, 'transitiontime': 0}}]

alert_green = [6, 0.5,
               {lighttypecolour  : {'on': True, 'bri': 255, 'xy': green, 'transitiontime': 0},
               lighttypedimmable: {'on': True, 'bri': 255, 'transitiontime': 0}},
               {lighttypecolour  : {'on': False, 'bri': 255, 'xy': green, 'transitiontime': 0},
               lighttypedimmable: {'on': False, 'bri': 10, 'transitiontime': 0}}]

allwhite = {lighttypecolour  : {'on': True, 'bri': 255, 'xy': white, 'transitiontime': 4},
            lighttypedimmable: {'on': True, 'bri': 255, 'transitiontime': 4}}

# If an alert is ongoing, this will be True
alert_in_progress = False

# Wait time between sending messages to the bridge - to stop congestion
waittime_default = 0.41


# = End of Setup ============================================================================

# -------------------------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------------------------

"""
Get the status of every light in the list of lights
Extend this if there are more light types in your network
Return Value: Dictionary of the status of all lights in the list
"""
def getlightstatus():
    light_status = {}
    for light in lights:
        light_type = b.get_light(light, 'type')
        if light_type == lighttypecolour:
            light_status.update({light: {'on' : b.get_light(light, 'on'),
                                        'bri': b.get_light(light, 'bri'),
                                        'xy' : b.get_light(light, 'xy')}})
        elif light_type == lighttypedimmable:
            light_status.update({light: {'on' : b.get_light(light, 'on'),
                                        'bri': b.get_light(light, 'bri')}})

    return light_status


"""
Return the status of the lights to what they were before the alert
Input: Dictionary of the status of all lights in the list (obtained from getlightstatus())
"""
def putlightstatus(light_status):
    global lights

    for light in lights:
        b.set_light(light, light_status[light])
        time.sleep(waittime_default)


# Runs through the alert dictionary defined in alert_pattern
# Input: alert_pattern containes the pre-defined alert pattern
def huealert(alert_pattern):
    global alert_in_progress, lighttype

    # Only run if we're not already in an alert
    if not alert_in_progress:
        alert_in_progress = True
        # Get the current status of the lamps
        preAlertStatus = getlightstatus()

        # Using the pre-defined alert patterns, change the lamp status
        for rep in range(alert_pattern[0]):
            for runalert in range(2, len(alert_pattern)):
                for light in lighttype:
                    b.set_light(light[0], alert_pattern[runalert][light[1]])
                    time.sleep(alert_pattern[1])

        # Return the lamps to the previous status
        putlightstatus(preAlertStatus)
        alert_in_progress = False


# Identifies if any of the lamps in the list are on
# Return Value: True if any lamps are on, otherwise False
def islampon():
    global alert_in_progress

    result = False

    if not alert_in_progress:
        islighton = getlightstatus()
        for light in lights:
            if islighton[light]['on']:
                result = True

    return result


# When the A button is pressed, run redalert
@touchphat.on_touch("A")
def toucha():
    huealert(alert_red)
    touchphat.led_off("A")


# When the B button is pressed, run alert_amber
@touchphat.on_touch("B")
def touchb():
    huealert(alert_amber)
    touchphat.led_off("B")


# When the C button is pressed, run alert_green
@touchphat.on_touch("C")
def touchc():
    huealert(alert_green)
    touchphat.led_off("C")


# When the D button is pressed, run alert_blue
@touchphat.on_touch("D")
def touchd():
    huealert(alert_blue)
    touchphat.led_off("D")


# When 'enter' is pressed, all lights are turned on to 'bright white'
# (i.e. what is defined in the dictionary 'allwhite'. Change at will.
@touchphat.on_touch("Enter")
def touchenter():
    global lighttype

    for light in lighttype:
        b.set_light(light[0], allwhite[light[1]])
        time.sleep(waittime_default)
    touchphat.led_off("Enter")
    touchphat.led_on("Back")


# When the Back button is pressed, toggle the lamp on/off status
@touchphat.on_touch("Back")
def touchback():
    global alert_in_progress

    if not alert_in_progress:
        lampon = islampon()
        alert_in_progress = True
        if lampon:
            for light in lights:
                b.set_light(light, 'on', False)
            touchphat.led_off("Back")
        else:
            for light in lights:
                b.set_light(light, 'on', True)
            touchphat.led_on("Back")
        time.sleep(1)
        alert_in_progress = False


# ================================================================
# Main loop - keep going forever
# ================================================================
while True:
    if alert_in_progress:
        time.sleep(1)
    else:
        if islampon():
            touchphat.led_on("Back")
        else:
            touchphat.led_off("Back")
        time.sleep(1)
