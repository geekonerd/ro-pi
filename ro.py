# GPIO
import RPi.GPIO as _g
# Keyboard input
import curses as _c
# time utilities
import time as _t

# configuration
from config import configuration as _conf
# servo motor for camera
from RoPiServo import RoPiServo
# motor for movements
from RoPiMotor import RoPiMotor
# leds
from RoPiLED import RoPiLED
# screen
#from RoPiScreen import RoPiScreen
# distance sensors
from RoPiDistance import RoPiDistance
# tracking sensors
from RoPiTrack import RoPiTrack

# start engines
if _conf['DEVEL_LOG'] : print("Starting engines...")
led = RoPiLED()
#screen = RoPiScreen()
distance = RoPiDistance(led)
track = RoPiTrack()
motor = RoPiMotor(distance, track)
servo = RoPiServo()
if _conf['DEVEL_LOG'] : print("Engines started!")

# capture commands from input
_s = _c.initscr()
_c.noecho()
_c.cbreak()
_s.keypad(True)
_s.nodelay(True)

# start infinite loop...
if _conf['DEVEL_LOG'] : print("Capturing input...")
started = _t.time()
try:
    while True:

        # capture input
        _k = _s.getch()

        if _conf['DEVEL_LOG'] : print("Captured key: ", _k)

        # pause/quit
        if _k == ord('p'):
            break

        # autonomus guide
        elif _k == ord('u'):
            motor.autonomous()

        # cam reset
        elif _k == ord('r'):
            servo.reset()

        # cam up
        elif _k == _c.KEY_UP:
            servo.up()

        # cam down
        elif _k == _c.KEY_DOWN:
            servo.down()

        # cam right
        elif _k == _c.KEY_RIGHT:
            servo.right()

        # cam left
        elif _k == _c.KEY_LEFT:
            servo.left()

        # wheels forward
        elif _k == ord('w'):
            motor.forward()

        # wheels backward
        elif _k == ord("s"):
            motor.backward()

        # wheels left
        elif _k == ord("a"):
            motor.forwardleft()

        # wheels right
        elif _k == ord("d"):
            motor.forwardright()

        # wheels left backward
        elif _k == ord("z"):
            motor.backwardleft()

        # wheels right backward
        elif _k == ord("x"):
            motor.backwardright()

        # clean old actions if no action in CLEAN_ACTION_TIME_SPAN
        elif _k == -1 :
            now = _t.time()
            if _conf['DEVEL_LOG'] : print("Nothing in time: ", now)
            if now - started > _conf['CLEAN_ACTION_TIME_SPAN'] :
                if _conf['DEVEL_LOG'] : print("Clean old queued actions...")
                motor.cleanQueues()
                led.allOff()
                started = _t.time()

# capture interruption
except KeyboardInterrupt:
    pass

# exit cycle
finally:
    _c.nocbreak()
    _s.keypad(0)
    _c.echo()
    _c.endwin()

# clean
servo.terminate()
motor.terminate()
#screen.terminate()
distance.terminate()
track.terminate()
_g.cleanup()
