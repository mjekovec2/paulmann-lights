#!/usr/bin/python3
# This little test program cycles your Paulmann LED 
# trough all available color temperatures and brightnesses

import pygatt
import logging
from time import sleep

from paulmann.paulmann import Paulmann
from paulmann.models import State, Info

#logging.basicConfig(level=logging.DEBUG)

# Find Paulmann device's MAC address using bluetoothctl or hcitool
# bluetoothctl scan on
MAC = "A0:B1:C3:D4:E5:F6"
PWD = "1234"

# Brightness can range from 0 - 100 percent
initial_brightness = 100

# Two color models are available 
# 153 - 370 (milireds)  370 = most warm
# or 2700 - 6500 (kelvin) 2700k = most warm
initial_color = 2700
min_color = 2700
max_color = 6500

# Reaction time of the LED/BT controller is quite slow.
# You might overload it's buffer if you send signals more frequently
interval=0.1
color_step=100
brightness_step=1

light = Paulmann(MAC, PWD, pygatt.backends.GATTToolBackend())
light.switch(True)
light.brightness(initial_brightness)
light.color_raw(initial_color)

state=light.get_state()
print("Status: " + str(state))

color =  int(state.color)
brightness = int(state.brightness)
new_color = int(color)
new_brightness = int(brightness)

while True:
    if (color + color_step) > max_color:
        new_color = max_color
        color_step = color_step * -1
    elif (color + color_step) < min_color:
        new_color = min_color
        color_step = color_step * -1
    else:
        new_color = color + color_step

    if (brightness + brightness_step) > 100:
        new_brightness = 100
        brightness_step = brightness_step * -1
    elif (brightness + brightness_step) < 1:
        new_brightness = 1
        brightness_step = brightness_step * -1
    else:
        new_brightness = brightness + brightness_step

    # Setting color and brightness simultanously with a value sanity check
    # (while in the background the values are set via bluethooth one after the other)
    # set_state(on=true) can also contain an "on" boolean attribute
    light.set_state(brightness=new_brightness, color=new_color)

    # Setting color and brightness individually with a value sanity check
    #light.brightness(new_brightness)
    #light.color(new_color)

    # Setting color and brightness without value sanity check
    #light.brightness_raw(new_brightness)
    #light.color_raw(new_color)

    brightness = new_brightness
    color = new_color
    sleep(interval)
