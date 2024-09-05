""" - python - micropytnon - """
# (C) 2023/2024 Joerg Jungermann, GPLv2 see LICENSE


# example:
#  * g = ColorBreed1D.game(n = 144)
#  * g.run()

DEAD = (0, 0, 0)

RGB = [
    (255,   0,   0),
    (  0, 255,   0),
    (  0,   0, 255),
]

class game:
    """ implementation of https://ee.hawaii.edu/~tep/EE205/Labs/Lab2/Life/1D_Life.html """

    def __init__(self, n = 15, pin = 0, palette = RGB, seed = None): # pylint: disable=dangerous-default-value
        from machine import Pin       # pylint: disable=import-error
        from neopixel import NeoPixel # pylint: disable=import-error
        import strip

        gpio = Pin(pin, Pin.OUT)
        self.np = NeoPixel(gpio, n)
        strip.off(self.np)

        if seed is None:
            self.randomSeed(palette)
            self.np.write()
        # FIXME: add code to pre-seed

    def randomSeed(self, palette = RGB):
        from random import getrandbits
        for i in range(0, len(self.np)):
            if getrandbits(1) == 1:
                self.np[i] = palette[i % len(palette)]
                #self.np[i] = palette[getrandbits(8) % len(palette)]
            else:
                self.np[i] = DEAD

    def step(self): # pylint: disable=missing-function-docstring
        neighbourMap = []
        for cell in range(0, len(self.np)): # build map of how many neigbours I have
            neighbourMap.append(self.neighbourCount(cell))

        for cell in range(0, len(self.np)):
            if not self.np[cell] == DEAD: # alive cell
                if neighbourMap[cell] in (0, 1, 3):
                    self.np[cell] = DEAD
                    #print ("%s dies (%s)" % (cell, neighbourMap[cell]))

            # dead cell
            elif neighbourMap[cell] in (2, 3):
                self.np[cell] = self.neighbourBreed(cell)
                #print ("%s born (%s)" % (cell, neighbourMap[cell]))

        self.np.write()

    def neighbourCount(self, cell):
        """ count alive neigbours != DEAD """
        n = len(self.np)
        cell = cell + n
        count = 0
        for i in [cell-2, cell-1, cell+1, cell+2]:
            if not self.np[i % n] == DEAD:
                count = count + 1
        return count

    def neighbourBreed(self, cell):
        """ mix all colours of alive neigbours != DEAD """
        n = len(self.np)
        cell = cell + n
        breed = list(self.np[(cell-2) % n])
        for i in [cell-1, cell+1, cell+2]:
            cellcolor = self.np[i % n]
            if not cellcolor == DEAD:
                breed[0] = (cellcolor[0] + breed[0]) // 2 | 1
                breed[1] = (cellcolor[1] + breed[1]) // 2 | 1
                breed[2] = (cellcolor[2] + breed[2]) // 2 | 1
        return breed

    def run(self, delay=20):          # pylint: disable=missing-function-docstring
        from time import sleep_ms     # pylint: disable=no-name-in-module
        while True:
            self.step()
            sleep_ms(delay)

    def print(self):
        for i in range(0, len(self.np)):
            if not self.np[i] == DEAD:
                print("%s: %s" % (i, self.np[i]))

# vim: noet ts=4 sw=4 ft=python foldmethod=indent
