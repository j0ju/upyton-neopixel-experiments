""" - python - micropytnon - """
# (C) 2023/2024 Joerg Jungermann, GPLv2 see LICENSE

import strip

GLIDER = ( ( 1, 1, 1 ),
           ( 1, 0, 0 ),
           ( 0, 1, 0 )
         )

# example:
#   import GameOfLife2D
#   g = GameOfLife2D.GameOfLife2D(seed=GameOfLife2D.GLIDER)

class GameOfLife2D:
    # pin = 5 ---> D1 on Wemos D1
    # pin = 5 ---> D3 on Seeed Studio ESP32-C3
    def __init__(self, x = 16, y = 16, pin = 5, dead = strip.BLACK, alive = strip.DIMWHITE, seed = None):
        from machine import Pin       # pylint: disable=import-error
        from neopixel import NeoPixel # pylint: disable=import-error

        self.x = x
        self.y = y
        n = x * y

        gpio = Pin(pin, Pin.OUT)
        self.np = NeoPixel(gpio, n)
        self.np_swap = NeoPixel(gpio, n)
        strip.off(self.np)

        self.DEAD = dead
        self.ALIVE = alive

        self.seed(seed)
    
        # be aware, we cannot use standard framebuffer calculations here on most WS2812 strips/fields
        # as they are enumbered as a snake on PCBs

        #  0   1   2   3   4   5  y = 0  ==> y % 2 == 0 ==> cell = py * y   + px
        # 11  10   9   8   7   6  y = 1  ==> y % 2 == 1 ==> cell = py * y+1 - px - 1
        # 12  13  14  15  16  17  y = 2
        # 18  19  20  21  22  23
    
    def xy2cell(self, x, y):
        sig = (1, -1)
        return (y+y%2) * self.y + sig[y%2] * (x+y%2)

    def seed(self, seed = None):
        if seed == None:
            from random import getrandbits
            # TODO: allow seeding of pre-defined data
            n = self.x * self.y
            for i in range(0, n):
                if getrandbits(1) == 1:
                    self.np[i] = self.ALIVE
                else:
                    self.np[i] = self.DEAD
        else:
            colormap = (self.DEAD, self.ALIVE)
            for x in range(0, self.x):
                for y in range(0, self.y):
                    try:
                        self.np[self.xy2cell(x,y)] = colormap[seed[x][y]]
                    except IndexError:
                        pass

        self.np.write()

    def step(self): # pylint: disable=missing-function-docstring
        for x in range(0, self.x):
            for y in range(0, self.y):
                neighbours = self.neighbourCount(x,y)
                cell = self.xy2cell(x, y)
                if not self.np[cell] == self.DEAD:
                    # starvation, under population
                    if neighbours < 2:
                       self.np_swap[cell] = self.DEAD
                    # over populatiom
                    elif neighbours > 3:
                        self.np_swap[cell] = self.DEAD
                    # i am feeling well, and alive
                    else:
                        self.np_swap[cell] = self.ALIVE
                else:
                    if neighbours == 3:
                        self.np_swap[cell] = self.ALIVE
                    else:
                        self.np_swap[cell] = self.DEAD

        tmp = self.np
        self.np = self.np_swap
        self.np_swap = tmp
        self.np.write()

    def neighbourCount(self, x, y): # pylint: disable=missing-function-docstring
        count = 0
        dx = -1
        for dx in  (-1, 0, 1):
            px = (x + dx) % self.x
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                py = (y + dy) % self.y
                if not self.np[self.xy2cell(px, py)] == self.DEAD:
                    count = count + 1
        return count

    def run(self, delay=30):          # pylint: disable=missing-function-docstring
        from time import sleep_ms     # pylint: disable=no-name-in-module
        while True:
            self.step()
            sleep_ms(delay)

# vim: noet ts=4 sw=4 ft=python
