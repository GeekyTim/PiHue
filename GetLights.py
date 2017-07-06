from phue import Bridge
import os.path
import time

bridgeip = '192.168.13.180'
b = Bridge(bridgeip)

if (os.path.exists("/home/pi/.python_hue")==False):
    print('Press the Hue`s connect button')
    b.connect()

lights = ['Test lamp']



lightstatus=[]
for light in lights:
    lightstatus.append([b.get_light(light, 'on'),
                        b.get_light(light, 'ct'),
                        b.get_light(light, 'sat'),
                        b.get_light(light, 'hue'),
                        b.get_light(light, 'xy')])
    print(b.get_light(light))


b.set_light('Test lamp', 'on', False)
time.sleep(3)
b.set_light('Test lamp', 'on', lightstatus[0][0])