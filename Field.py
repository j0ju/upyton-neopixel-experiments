""" - python - micropytnon - """
# (C) 2023/2024 Joerg Jungermann, GPLv2 see LICENSE

import strip

class Field:

    def __init__(self, x = 16, y = 16, pin = 5):
        from machine import Pin       # pylint: disable=import-error
        from neopixel import NeoPixel # pylint: disable=import-error

        print("Field::__init__(): %s/%s pin=%s)" % (x, y, pin))

        self.X = x
        self.Y = y
        n = x * y

        gpio = Pin(pin, Pin.OUT)
        self.np = NeoPixel(gpio, n)
        self.Wipe()

    # be aware, we cannot use standard framebuffer calculations here on most WS2812 strips/fields
    # as they are enumbered as a snake on PCBs
    #  0   1   2   3   4   5  y = 0  ==> y % 2 == 0 ==> cell = py * y   +  px
    # 11  10   9   8   7   6  y = 1  ==> y % 2 == 1 ==> cell = py * y+1 - (px + 1)
    # 12  13  14  15  16  17  y = 2
    # 18  19  20  21  22  23
    def xy2cell(self, x, y):
        signum = (1, -1)
        return (y+y%2) * self.Y + signum[y%2] * (x+y%2)

    def __getitem__(self, k):
        return self.np[self.xy2cell(k[0],k[1])]

    def __setitem__(self, k, v):
        self.np[self.xy2cell(k[0],k[1])] = v

    def Wipe(self):
        strip.off(self.np)

    def Fill(self, xmin, ymin, xmax, ymax, color):
        for x in range(xmin, xmax):
            for y in range(ymin, ymax):
                self[x,y] = color
        self.Update()

    def Update(self):
        self.np.write()

