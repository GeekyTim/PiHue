#!/usr/bin/python3

# Import libraries
# Install phue and touchphat with pip3
# pip3 install phue
# pip3 install touchphat
from phue import Bridge
import touchphat
import os.path

# Setup
touchphat.all_off()

bridgeip = '192.168.13.180'


b = Bridge(bridgeip)



#If running for the first time, press button on bridge and run with b.connect() uncommented
if (os.path.exists("~/.python_hue")==False):
    print('Press the Hue`s connect button')
    b.connect()

#