# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Stuff you need to change!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""
Hue 'xy' colours - expand at will
"""
red = (0.675, 0.322)
green = (0.4091, 0.518)
blue = (0.167, 0.04)
yellow = (0.4325035269415173, 0.5007488105282536)
blueviolet = (0.2451169740627056, 0.09787810393609737)
orange = (0.6007303214398861, 0.3767456073628519)
white = (0.32272672086556803, 0.3290229095590793)

"""
Alert Patterns
Used to change the status of lights
The first number is the number of repeat cycles. 
The second is the delay between changes.
The following dictionaries are the change of light status.
Use any valid HUE setting - e.g. on, bri, xy, ct, sat, hue, transformationtime
But remember that dimmable lamps only dim ('bri') and don't change colour ('no 'xy')
"""
alert_red = [6, 1.0,
             {'on': True, 'bri': 255, 'xy': red},
             {'on': False}]

alert_amber = [6, 1.0,
               {'on': True, 'bri': 255, 'xy': orange},
               {'on': False}]

alert_green = [6, 1.0,
               {'on': True, 'bri': 255, 'xy': green},
               {'on': False}]

alert_blue = [6, 1.0,
              {'on': True, 'bri': 255, 'xy': blue},
              {'on': False}]

# For turning the lights all on to bright white
allwhite = {'on': True, 'bri': 255, 'xy': white}
