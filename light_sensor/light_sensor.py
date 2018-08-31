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

    delay = 60 * 7
    # delay = 5
    last_activation = -1.

    while True:
        if io.input(pin) == 1:
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

        time.sleep(.1)


if __name__ == "__main__":
    main()
