""" - python - micropytnon - """
# (C) 2023/2024 Joerg Jungermann, GPLv2 see LICENSE

import strip

# example:
#  * g = GameOfLife1D.GameOfLife1D(n = 144)
#  * g.run()

class GameOfLife1D:
    """ implementation of https://ee.hawaii.edu/~tep/EE205/Labs/Lab2/Life/1D_Life.html """

    def __init__(self, n = 15, pin = 0, dead = strip.BLACK, alive = (16, 16, 16), seed = None):
        from machine import Pin       # pylint: disable=import-error
        from neopixel import NeoPixel # pylint: disable=import-error
        from random import getrandbits

        gpio = Pin(pin, Pin.OUT)
        self.np = NeoPixel(gpio, n)
        strip.off(self.np)

        self.DEAD = dead
        self.ALIVE = alive

        if seed is None:
            for i in range(0, n):
                if getrandbits(1) == 1:
                    self.np[i] = alive
                else:
                    self.np[i] = dead
            self.np.write()
        # FIXME: add code to pre-seed

    def step(self): # pylint: disable=missing-function-docstring
        neighbourMap = []
        for cell in range(0, len(self.np)): # build map of how many neigbours I have
            neighbourMap.append(self.neighbourCount(cell))
            #print ("%s: %s" % (cell, neighbourMap[cell]))

        for cell in range(0, len(self.np)):
            if not self.np[cell] == strip.BLACK: # alive cell
                if neighbourMap[cell] in (0, 1, 3):
                    self.np[cell] = self.DEAD
                    #print ("%s dies (%s)" % (cell, neighbourMap[cell]))

            else: # dead cell
                if neighbourMap[cell] in (2, 3):
                    self.np[cell] = self.ALIVE
                    #print ("%s born (%s)" % (cell, neighbourMap[cell]))

        self.np.write()

    def neighbourCount(self, cell): # pylint: disable=missing-function-docstring
        n = len(self.np)
        count = 0
        for i in [cell-2, cell-1, cell+1, cell+2]:
            if not self.np[(i + n) % n] == strip.BLACK:
                count = count + 1
        return count

    def run(self, delay=30):          # pylint: disable=missing-function-docstring
        from time import sleep_ms     # pylint: disable=no-name-in-module
        while True:
            self.step()
            sleep_ms(delay)

# vim: noet ts=4 sw=4 ft=python
