BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

RAINBOW = [ # https://wiki.baw.de/de/index.php/Farbverlauf:_Regenbogen,_29_Farben
    (128,   0,   0),
    (130,  40,  40),
    (141,  83,  59),
    (153, 102, 117),
    (153, 102, 169),
    (128,   0, 128),
    (101,   0, 155),
    ( 72,   0, 225),
    (  4,   0, 208),
    (  0,  68, 220),
    (  1, 114, 226),
    (  1, 159, 232),
    ( 11, 175, 162),
    ( 23, 179,  77),
    (  0, 212,  28),
    (  0, 255,   0),
    (128, 255,   0),
    (200, 255,   0),
    (255, 255,   0),
    (255, 219,   0),
    (255, 182,   0),
    (255, 146,   0),
    (255, 109,   0),
    (255,  73,   0),
    (255,   0,   0),
    (255,   0, 128),
    (255, 105, 180),
    (255,   0, 255),
    (168,   0, 185)
]

def wanderingPixel(color = WHITE, n = 15, back = BLACK, pin = 0, delay_ms = 50):
    from machine import Pin
    from neopixel import NeoPixel
    from time import sleep_ms

    gpio = Pin(pin, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
    np = NeoPixel(gpio, n)   # create NeoPixel driver on GPIO0 for 8 pixels
    n = n - 1

    i = 0
    step = -1

    try:
        while True:
            np[i] = back
            if i == 0 or i == n:
                step = step * -1
            i = i + step
            np[i] = color
            np.write()
            sleep_ms(delay_ms)
    except KeyboardInterrupt as e:
        fill(np, BLACK)
        raise(e)

def movingPaint(colors, n = 15, pin = 0, delay_ms = 100):
    from machine import Pin
    from neopixel import NeoPixel
    from time import sleep_ms

    gpio = Pin(pin, Pin.OUT)
    np = NeoPixel(gpio, n)
    ncolors = len(colors)
    istart = 0

    try:
        while True:
            paint(np, colors, istart = istart)
            istart = (istart + 1) % ncolors
            sleep_ms(delay_ms)
    except KeyboardInterrupt as e:
        fill(np, BLACK)
        raise(e)

def fill(np, color):
    for  i in range(0, np.n):
        np[i] = color
    np.write()

def paint(np, colors, istart = 0):
    ncolors = len(colors)
    for  i in range(0, np.n):
        np[i] = colors[(istart + i) % ncolors]
    np.write()
