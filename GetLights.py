from phue import Bridge
import os.path
import time

bridgeip = '192.168.13.180'
b = Bridge(bridgeip)

if (os.path.exists("~/.python_hue")==False):
    print('Press the Hue`s connect button')
    b.connect()

lights = ['Test lamp']

for light in lights:

    print(b.get_light(light))
    print(b.get_light(light, 'on'))
    print(b.get_light(light, 'ct'))
    print(b.get_light(light, 'xy'))
    print(b.get_light(light, 'sat'))
    print(b.get_light(light, 'hue'))

ls = b.get_light('Test lamp')

b.set_light('Test lamp', 'on', False)
time.sleep(1)
b.set_light('Test lamp', 'on', ls['on'])