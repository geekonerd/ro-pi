# GPIO
import RPi.GPIO as _g
# time utilities
import time as _t
# multiprocessing
import multiprocessing as _mp

# ADAfruit library
from Adafruit_CharLCD import *

# configuration
from config import screen_conf as _conf

# RO-PI SCREEN
class RoPiScreen:

    # initialize
    def __init__(self) :

        # set PINs on BOARD
        if _conf['DEVEL_LOG'] : print("Initializing Screen...")
        self.lcd = Adafruit_CharLCD(
            _conf['lcd_rs'],
            _conf['lcd_en'],
            _conf['lcd_d4'],
            _conf['lcd_d5'],
            _conf['lcd_d6'],
            _conf['lcd_d7'],
            _conf['lcd_columns'], 
            _conf['lcd_rows'],
            _conf['lcd_backlight'])

        # directions
        if _conf['DEVEL_LOG'] :
            print("Initializing queues and processes...")
        self.queue = _mp.Queue()
        self.process = _mp.Process(target=self.S)
        self.process.start()

        if _conf['DEVEL_LOG'] : print("...init done!")

    # control Screen
    def S(self) :
        while True :
            if not self.queue.empty() :
                message = self.queue.get().split("|")
                duration = float(message[1])
                message = message[0]
                if _conf['DEVEL_LOG'] : print("Message to show: ", message)
                self.lcd.message(message)
                _t.sleep(duration)
                self.clearScreen()

    # terminate
    def terminate(self) :
        if _conf['DEVEL_LOG'] : print("Screen termination...")
        self.clearScreen()
        self.clearQueue(self.queue)
        self.process.terminate()

    # clean queue
    def clearQueue(self, q) :
        while not q.empty() :
            q.get()

    # clear screen
    def clearScreen(self) :
        self.lcd.clear()

    # actions
    def showMessage(self, message, duration) :
        self.queue.put(message + "|" + duration)

# DEBUG
if __name__ == "__main__":
    print ("Testing Screen...")
    screen = RoPiScreen()
    screen.message("TEST", 2)
