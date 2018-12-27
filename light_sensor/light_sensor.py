#!/usr/bin/env python3

import time

import RPi.GPIO as io
from yeelight import Bulb, BulbException


def toggle():
    io.setmode(io.BOARD)
    pin = 7
    io.setup(pin, io.IN)

    light_ip = "192.168.178.31"
    bulb = Bulb(light_ip)
    bulb.turn_off()

    last_input = -1
    last_toggle = -1.
    cool_down = 2  # seconds
    time_out = 30 * 60
    is_on = False

    while True:
        now = time.time()
        this_input = io.input(pin)
        if this_input == 1 and last_input == 0 and now - last_toggle >= cool_down:
            try:
                if is_on:
                    bulb.turn_off()
                else:
                    bulb.turn_on()
                is_on = not is_on
                last_toggle = now

            except BulbException:
                pass

        elif is_on and now - last_toggle >= time_out:
            try:
                bulb.turn_off()
                is_on = False

            except BulbException:
                pass

        last_input = this_input
        time.sleep(.1)


def keep_on():
    io.setmode(io.BOARD)
    pin = 7
    io.setup(pin, io.IN)

    light_ip = "192.168.178.31"
    bulb = Bulb(light_ip)
    bulb.turn_off()

    delay = 30 * 8
    # delay = 5
    last_activation = -1.

    while True:
        activation = io.input(pin)

        if activation == 1:
            try:
                if last_activation < 0:
                    bulb.turn_on()
                last_activation = time.time()
            except BulbException:
                pass

        if last_activation >= 0. and time.time() - last_activation >= delay:
            try:
                bulb.turn_off()
                last_activation = -1.
            except BulbException:
                pass

        print(activation)

        time.sleep(.1)


if __name__ == "__main__":
    keep_on()
    # toggle()
