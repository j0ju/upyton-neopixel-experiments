from math import sin, pi, floor
from random import randint
from NeoPixelField import NeoPixelField
from time import sleep_ms     
import strip

class Heartbeat(NeoPixelField):	
    # pin = 5 ---> D1 on Wemos D1
    # pin = 5 ---> D3 on Seeed Studio ESP32-C3
    def Sine(self, dx = 0, color=strip.DIMWHITE, Update = True):
        oddity = self.Y % 2 - 1 # { odd, even } --> { 0 , -1 } - offset for even Y
        scale = self.Y / 2 + oddity
        bias = self.Y / 2 + oddity 
        for x in range(0, self.X):
            y = floor(sin(2*pi/(self.X)*((x+dx)%self.X))*scale+bias)
            self[x,y] = color
        if Update:
            self.Update()

    
    def WanderingSine(self, delay=30):
        dx = 0
        while True:
            self.Sine(dx = dx, color = strip.BLACK, Update = False)
            dx += 1
            dx %= self.X
            self.Sine(dx = dx)
            sleep_ms(delay)

    def RandomBoxes(self, palette, delay=30):
        while True:
            xmin = randint(0, self.X-1)
            ymin = randint(0, self.Y-1)
            xmax = randint(xmin, self.X-1)
            ymax = randint(ymin, self.Y-1)
            colorindex = randint(0, len(palette)-1)
            self.Fill(xmin, ymin, xmax, ymax, palette[colorindex])
            sleep_ms(delay)

# vim: noet ts=4 sw=4 ft=python foldmethod=indent
