# GPIO
import RPi.GPIO as _g
# time utilities
import time as _t

# configuration
from config import led_conf as _conf

# RO-PI LED SENSORS
class RoPiLED:

    # initialize
    def __init__(self) :

        # set PINs on BOARD
        if _conf['DEVEL_LOG'] :
            print("Initializing LEDs...")
            print("> RED:", _conf['red_pin'])
            print("> GREEN:", _conf['green_pin'])
            print("> BLUE:", _conf['blue_pin'])
        _g.setmode(_g.BOARD)
        _g.setup(_conf['red_pin'], _g.OUT) # output, blink red
        _g.setup(_conf['green_pin'], _g.OUT) # output, blink green
        _g.setup(_conf['blue_pin'], _g.OUT) # output, blink blue

        if _conf['DEVEL_LOG'] : print("...init done!")

    # activate pin
    def activate(self, p) :
        _g.output(p, _g.HIGH)

    # deactivate pin
    def deactivate(self, p) :
        _g.output(p, _g.LOW)

    # actions
    def allOff(self) :
        self.redOff()
        self.greenOff()
        self.blueOff()
    def redOn(self) :
        self.activate(_conf['red_pin'])
    def redOff(self) :
        self.deactivate(_conf['red_pin'])
    def greenOn(self) :
        self.activate(_conf['green_pin'])
    def greenOff(self) :
        self.deactivate(_conf['green_pin'])
    def blueOn(self) :
        self.activate(_conf['blue_pin'])
    def blueOff(self) :
        self.deactivate(_conf['blue_pin'])
    def yellowOn(self) :
        self.redOn()
        self.greenOn()
    def yellowOff(self) :
        self.redOff()
        self.greenOff()
    def cyanOn(self) :
        self.greenOn()
        self.blueOn()
    def cyanOff(self) :
        self.greenOff()
        self.blueOff()
    def magentaOn(self) :
        self.redOn()
        self.blueOn()
    def magentaOff(self) :
        self.redOff()
        self.blueOff()
    def whiteOn(self) :
        self.redOn()
        self.greenOn()
        self.blueOn()
    def whiteOff(self) :
        self.redOff()
        self.greenOff()
        self.blueOff()

# DEBUG
if __name__ == "__main__":
    print ("Welcome! Testing LED:")
    time = 1
    led = RoPiLED()
    print ("White...")
    led.whiteOn()
    _t.sleep(time)
    led.whiteOff()
    print ("Magenta...")
    led.magentaOn()
    _t.sleep(time)
    led.magentaOff()
    print ("Cyan...")
    led.cyanOn()
    _t.sleep(time)
    led.cyanOff()
    print ("Yellow...")
    led.yellowOn()
    _t.sleep(time)
    led.yellowOff()
    print ("Blue...")
    led.blueOn()
    _t.sleep(time)
    led.blueOff()
    print ("Green...")
    led.greenOn()
    _t.sleep(time)
    led.greenOff()
    print ("Red...")
    led.redOn()
    _t.sleep(time)
    led.redOff()
    print ("Goodbye!")
    led.allOff()
    _g.cleanup()
