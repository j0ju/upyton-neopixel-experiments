""" micropython - boot.py -- run on boot-up """

# increase CPU speed of Wemos D1/ESP8266
#from machine import freq
#freq(160000000)

# clear LED (with 200 LEDs on PIN0) strip on boot, this eats some memory
#try:
#    import strip
#    from machine import Pin
#    from neopixel import NeoPixel
#    pin = 0
#    n = 200
#    gpio = Pin(pin, Pin.OUT)
#    np = NeoPixel(gpio, n)
#    strip.off(np)
#except Exception as e:
#    raise(e)

# vim: noet ts=4 sw=4 ft=python
