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
    def __init__(self, x = 16, y = 16, pin = 5, dead = strip.BLACK, alive = strip.DIMWHITE, dying = strip.DIMWHITE, born = strip.DIMWHITE, forecast = strip.BLACK, seed = None):
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
        self.DYING = dying
        self.BORN = born
        self.FORECAST = forecast

        self.world = []
        self.lastGeneration = []
        for y in range(0, self.y):
            self.world.append([])
            self.lastGeneration.append([])
            for x in range(0, self.x):
                self.world[y].append(0)
                self.lastGeneration[y].append(0)

        self.seed(seed)
    
    # be aware, we cannot use standard framebuffer calculations here on most WS2812 strips/fields
    # as they are enumbered as a snake on PCBs
    #  0   1   2   3   4   5  y = 0  ==> y % 2 == 0 ==> cell = py * y   +  px
    # 11  10   9   8   7   6  y = 1  ==> y % 2 == 1 ==> cell = py * y+1 - (px + 1)
    # 12  13  14  15  16  17  y = 2
    # 18  19  20  21  22  23
    def xy2cell(self, x, y):
        signum = (1, -1)
        return (y+y%2) * self.y + signum[y%2] * (x+y%2)

    # seed world and prepare world array for swaping
    def seed(self, seed = None):
        from random import getrandbits
        for y in range(0, self.y):
            for x in range(0, self.x):
                if seed == None:
                    self.world[y][x] = getrandbits(1)
                else:
                    try:
                        v = seed[x][y]
                        self.world[y][x] = v
                    except IndexError:
                        pass
        self.display()

    def display(self):
        m = (self.DEAD, self.ALIVE)
        for y in range(0, self.y):
            for x in range(0, self.x):
                if self.world[y][x] == 1:
                    if self.lastGeneration[y][x] == 0:
                        self.np[self.xy2cell(x,y)] = self.BORN
                    elif self.nextState(x,y) == 0:
                        self.np[self.xy2cell(x,y)] = self.DYING
                    else:
                        self.np[self.xy2cell(x,y)] = m[self.world[y][x]]
                else:
                    if self.nextState(x,y) == 1:
                        self.np[self.xy2cell(x,y)] = self.FORECAST
                    else:
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

    def nextState(self, x, y):
        neighbours = self.neighbourCount(x,y)
        if self.world[y][x] == 1:
            # starvation, under population
            if neighbours < 2:
                return 0
            # over populatiom
            elif neighbours > 3:
                return 0
            # i am feeling well, and alive
            else:
                return 1
        else:
            if neighbours == 3:
                return 1
            else:
                return 0

    def step(self): # pylint: disable=missing-function-docstring
        nextGeneration = self.lastGeneration
        for x in range(0, self.x):
            for y in range(0, self.y):
                nextGeneration[y][x] = self.nextState(x, y)

        self.lastGeneration = self.world
        self.world = nextGeneration
        self.display()

    def populationCount(self):
        c = 0
        for x in range(0, self.x):
            for y in range(0, self.y):
                c = c + self.world[y][x]
        return c

    def run(self, delay=30):          # pylint: disable=missing-function-docstring
        from time import sleep_ms     # pylint: disable=no-name-in-module
        population = self.populationCount()
        lastPopulation = 0
        while True:
            #if population == lastPopulation:
            #    self.seed()
            #lastPopulation = population
            self.step()
            population = self.populationCount()
            sleep_ms(delay)

# vim: noet ts=4 sw=4 ft=python
