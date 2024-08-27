""" - python - micropytnon - """
# (C) 2023/2024 Joerg Jungermann, GPLv2 see LICENSE

import strip

GLIDER = ( ( 1, 1, 1 ),
           ( 1, 0, 0 ),
           ( 0, 1, 0 )
         )

SPACESHIP = ( ( 1, 0, 0, 1, 0),
              ( 0, 0, 0, 0, 1),
              ( 1, 0, 0, 0, 1),
              ( 0, 1, 1, 1, 1)
            )

# example:
#   import GameOfLife2D
#   g = GameOfLife2D.GameOfLife2D(seed=GameOfLife2D.GLIDER)
#   g = GameOfLife2D.GameOfLife2D(seed=GameOfLife2D.SPACESHIP)
#   g.run()

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
        strip.off(self.np)

        self.DEAD = dead
        self.ALIVE = alive

        self.seed(seed)
        self.display()
    
    # be aware, we cannot use standard framebuffer calculations here on most WS2812 strips/fields
    # as they are enumbered as a snake on PCBs
    #  0   1   2   3   4   5  y = 0  ==> y % 2 == 0 ==> cell = py * y   + px
    # 11  10   9   8   7   6  y = 1  ==> y % 2 == 1 ==> cell = py * y+1 - px - 1
    # 12  13  14  15  16  17  y = 2
    # 18  19  20  21  22  23
    def xy2cell(self, x, y):
        sig = (1, -1)
        return (y+y%2) * self.y + sig[y%2] * (x+y%2)

    # seed world and prepare world array for swaping
    def seed(self, seed = None):
        from random import getrandbits
        self.world = []
        self.swap = []
        for y in range(0, self.y):
            self.world.append([])
            self.swap.append([])
            for x in range(0, self.x):
                if seed == None:
                    self.world[y].append(getrandbits(1))
                else:
                    try:
                        self.world[y].append(seed[x][y])
                    except IndexError:
                        self.world[y].append(0)
                self.swap[y].append(0)

    def display(self):
        m = (self.DEAD, self.ALIVE)
        for y in range(0, self.y):
            for x in range(0, self.x):
                self.np[self.xy2cell(x,y)] = m[self.world[y][x]]
        self.np.write()

    def neighbourCount(self, x, y): # pylint: disable=missing-function-docstring
        count = 0
        for dx in (-1, 0, 1):
            px = (x + dx) % self.x
            for dy in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                py = (y + dy) % self.y
                count = count + self.world[py][px]
        return count

    def step(self): # pylint: disable=missing-function-docstring
        for x in range(0, self.x):
            for y in range(0, self.y):
                neighbours = self.neighbourCount(x,y)
                if self.world[y][x] == 1:
                    # starvation, under population
                    if neighbours < 2:
                       self.swap[y][x] = 0
                    # over populatiom
                    elif neighbours > 3:
                       self.swap[y][x] = 0
                    # i am feeling well, and alive
                    else:
                       self.swap[y][x] = 1
                else:
                    if neighbours == 3:
                       self.swap[y][x] = 1
                    else:
                       self.swap[y][x] = 0

        tmp = self.world
        self.world = self.swap
        self.swap = tmp
        self.display()

    def run(self, delay=30):          # pylint: disable=missing-function-docstring
        from time import sleep_ms     # pylint: disable=no-name-in-module
        while True:
            self.step()
            sleep_ms(delay)

# vim: noet ts=4 sw=4 ft=python
