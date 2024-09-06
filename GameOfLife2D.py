""" - python - micropytnon - """
# (C) 2023/2024 Joerg Jungermann, GPLv2 see LICENSE

import strip
from NeoPixelField import NeoPixelField

# b'#' - alive
# b'.' - dead
# b'_' - don't touch

GLIDER = b"""
    .....
    .###.
    .#...
    ..#..
    .....
"""

SPACESHIP = b"""
    .......
    .#..#..
    .....#.
    .#...#.
    ..####.
    .......
"""

# example:
#   import GameOfLife2D; g = GameOfLife2D.GameOfLife2D(); g.Run()
# preseeds:
#   g = GameOfLife2D.GameOfLife2D(seed=GameOfLife2D.GLIDER)
#   g = GameOfLife2D.GameOfLife2D(seed=GameOfLife2D.SPACESHIP)

class GameOfLife2D(NeoPixelField):
    # pin = 5 ---> D1 on Wemos D1
    # pin = 5 ---> D3 on Seeed Studio ESP32-C3
    def __init__(self, x = 16, y = 16, pin = 5, dead = strip.BLACK, alive = strip.DIMWHITE, dying = strip.DIMWHITE, born = strip.DIMWHITE, forecast = strip.BLACK, seed = None):
        print("GameOfLife2D::__init__(): %s/%s pin=%s)" % (x, y, pin))
        super().__init__(x = x, y = y, pin = pin)

        self.DEAD = dead
        self.ALIVE = alive
        self.DYING = dying
        self.BORN = born
        self.FORECAST = forecast

        self.Wipe()
        self.Seed(seed)

    def Wipe(self):
        self.world = []
        self.lastGeneration = []
        self.lastLastGeneration = []
        for y in range(0, self.Y):
            self.world.append([])
            self.lastGeneration.append([])
            self.lastLastGeneration.append([])
            for x in range(0, self.X):
                self.world[y].append(0)
                self.lastGeneration[y].append(1)
                self.lastLastGeneration[y].append(0)
        super().Wipe()
    
    # seed world and prepare world array for swaping
    def Seed(self, seed = None, dx = 0, dy = 0):
        print("Seed()")
        if seed == None:
            from random import getrandbits
            for y in range(0, self.Y):
                for x in range(0, self.X):
                    self.world[(y+dy)%self.Y][(x+dx)%self.X] = getrandbits(1)
        else:
            y = 0
            for l in seed.strip().split(b'\n'):
                x = 0
                py = ( y + dy ) % self.Y
                l = l.strip()
                #print("y=%s %s" % (y, l))
                for ch in l:
                    v = None
                    px = ( x + dx ) % self.X
                    if ch == 35: # b'#'
                        v=1
                    elif ch == 46: # b'.'
                        v=0
                    #print("%s/%s => %s/%s = b'%s' = %s" % (x,y, px, py, str(ch), v))
                    if not v == None:
                        self.world[py][px] = v
                        self.lastLastGeneration[py][px] = (v+1)%2
                    x += 1

                y += 1

        self.Display()

    # TODO: sync == False is broken for speed up
    def Display(self, sync = True):
        for y in range(0, self.Y):
            for x in range(0, self.X):
                if sync or not self.world[y][x] == self.lastGeneration[y][x]:
                    if self.world[x][y] == 1:
                        if self.lastGeneration[y][x] == 0:
                            self[x,y] = self.BORN
                        elif self.nextState(x,y) == 0:
                            self[x,y] = self.DYING
                        else:
                            self[x,y] = self.ALIVE
                    else:
                        if self.nextState(x,y) == 1:
                            self[x,y] = self.FORECAST
                        else:
                            self[x,y] = self.DEAD
        self.Update()

    def neighbourCount(self, x, y): # pylint: disable=missing-function-docstring
        count = 0
        for dx in (-1, 0, 1):
            px = (x + dx) % self.X
            for dy in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                py = (y + dy) % self.Y
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

    def Step(self): # pylint: disable=missing-function-docstring
        nextGeneration = self.lastLastGeneration
        for x in range(0, self.X):
            for y in range(0, self.Y):
                nextGeneration[y][x] = self.nextState(x, y)

        self.lastLastGeneration = self.lastGeneration
        self.lastGeneration = self.world
        self.world = nextGeneration
        self.Display()

    def populationCount(self):
        c = 0
        for x in range(0, self.X):
            for y in range(0, self.Y):
                c = c + self.world[y][x]
        return c

    def compareWorld(self, w1, w2):
        for y in range(0, self.Y):
            for x in range(0, self.X):
                if not w1[y][x] == w2[y][x]:
                    return False
        return True

    def Run(self, delay=30):          # pylint: disable=missing-function-docstring
        from time import sleep_ms     # pylint: disable=no-name-in-module
        population = self.populationCount()
        lastPopulation = 0
        lastLastPopulation = 0
        iterations = 0
        while True:
            # re-seed decisions
            # detect empty playfield
            if population == 0:
                print("Run(): pop == 0, %s iterations" % iterations)
                self.Seed()
                iterations = 0
            # detect 1-cycle or 2-cycles
            elif population == lastLastPopulation:
                #print("Run(): pop == lastLastPop")
                if self.compareWorld(self.world, self.lastLastGeneration):
                    print("Run(): 2-cycle detected, %s iterations" % iterations)
                    self.Seed()
                    iterations = 0

            lastLastPopulation = lastPopulation
            lastPopulation = population

            self.Step()
            population = self.populationCount()
            iterations = iterations + 1
            sleep_ms(delay)

# vim: noet ts=4 sw=4 ft=python foldmethod=indent
