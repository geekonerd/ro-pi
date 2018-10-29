# GPIO
import RPi.GPIO as _g
# time utilities
import time as _t
# multiprocessing
import multiprocessing as _mp

# configuration
from config import distance_conf as _conf

# RO-PI DISTANCE SENSORS
class RoPiDistance:

    # initialization
    def __init__(self, led) :

        # set PINs on BOARD
        if _conf['DEVEL_LOG'] :
            print("Initializing Distance...")
            print("> echo 1", _conf['echo_1_pin'])
            print("> trig 1", _conf['trig_1_pin'])
            print("> echo 2", _conf['echo_2_pin'])
            print("> trig 2", _conf['trig_2_pin'])
        _g.setmode(_g.BOARD)
        _g.setup(_conf['trig_1_pin'], _g.OUT) # output: send signal
        _g.setup(_conf['echo_1_pin'], _g.IN) # input: receive result
        _g.setup(_conf['trig_2_pin'], _g.OUT) # output: send signal
        _g.setup(_conf['echo_2_pin'], _g.IN) # input: receive result

        # metrics
        self.distance1 = _mp.Value('i', 0)
        self.distance2 = _mp.Value('i', 0)
        self.close = _mp.Value('i', 0)

        # initialize LED
        self.led = led

        # processes
        if _conf['DEVEL_LOG'] : print("Initializing processes...")
        self.process1 = _mp.Process(target=self.D1)
        self.process2 = _mp.Process(target=self.D2)
        self.process1.start()
        self.process2.start()

        if _conf['DEVEL_LOG'] : print("...init done!")

    # terminate
    def terminate(self) :
        if _conf['DEVEL_LOG'] : print("Distance termination...")
        self.process1.terminate()
        self.process2.terminate()

    # activate pin
    def activate(self, p) :
        _g.output(p, _g.HIGH)

    # deactivate pin
    def deactivate(self, p) :
        _g.output(p, _g.LOW)

    # retrieve metrics
    def isClose(self) :
        if _conf['DEVEL_LOG'] : print("> isClose? ", self.close.value)
        return self.close.value
    def getDistance1(self) :
        if _conf['DEVEL_LOG'] : print("> distance1: ", self.distance1.value)
        return self.distance1.value
    def getDistance2(self) :
        if _conf['DEVEL_LOG'] : print("> distance2: ", self.distance2.value)
        return self.distance2.value

    # control distance sensor 1
    def D1(self) :
        self.worker(_conf['trig_1_pin'], _conf['echo_1_pin'], self.distance1, 0)

    # control distance sensor 1
    def D2(self) :
        self.worker(_conf['trig_2_pin'], _conf['echo_2_pin'], self.distance2, 1)

    # worker
    def worker(self, trigPin, echoPin, distance, color) :
        while True :
            _t.sleep(_conf['SENSORS_OFF_SPAN'])
            self.activate(trigPin)
            _t.sleep(_conf['TRIG_SPAN'])
            self.deactivate(trigPin)
            distance.value = self.calculate_distance(
                self.wait_for_signal(_t.time(), echoPin),
                self.wait_for_distance(_t.time(), echoPin))
            if (distance.value < _conf['SAFETY_DISTANCE']) :
                self.close.value = 1
                if not self.led == False :
                    if color == 0 :
                        self.led.redOn()
                    else :
                        self.led.blueOn()
            else :
                self.close.value = 0
                if not self.led == False :
                    if color == 0 :
                        self.led.redOff()
                    else :
                        self.led.blueOff()

    # wait for pulse start
    def wait_for_signal(self, pulse_start, pin) :
        while _g.input(pin) == 0 :
           pulse_start = _t.time()
        return pulse_start

    # wait for pulse end
    def wait_for_distance(self, pulse_end, pin) :
        while _g.input(pin) == 1 :
           pulse_end = _t.time()
        return pulse_end

    # calculate distance
    def calculate_distance(self, pulse_start, pulse_end) :
       pulse_duration = pulse_end - pulse_start
       distance = pulse_duration * _conf['SPEED_OF_SOUND']
       return int(distance)

# DEBUG
if __name__ == "__main__":
    print ("Welcome! Testing Distance Sensors:")
    print ("Safety distance: ", _conf['SAFETY_DISTANCE'])
    time = 1
    distance = RoPiDistance(False)
    try:
        while True:
            print("Distance1: ", distance.getDistance1())
            print("Distance2: ", distance.getDistance2())
            print("isClose: ", distance.isClose())
            _t.sleep(time)
    except KeyboardInterrupt:
        pass
    print ("Goodbye!")
    distance.terminate()
    _g.cleanup()
