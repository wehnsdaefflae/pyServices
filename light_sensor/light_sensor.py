#!/usr/bin/env python3

import time

import RPi.GPIO as io
from yeelight import Bulb, BulbException


def main():
    io.setmode(io.BOARD)
    pin = 7
    io.setup(pin, io.IN)

    light_ip = "192.168.178.31"
    bulb = Bulb(light_ip)
    bulb.turn_off()

    delay = 60 * 5
    # delay = 5
    last_activation = -1.

    while True:
        if io.input(pin) == 1 and last_activation < 0.:
            try:
                last_activation = time.time()
                bulb.turn_on()
            except BulbException:
                pass

        if last_activation >= 0. and time.time() - last_activation >= delay:
            try:
                last_activation = -1.
                bulb.turn_off()
            except BulbException:
                pass

        time.sleep(.1)


if __name__ == "__main__":
    main()
