# GPIO
import RPi.GPIO as _g
# time utilities
import time as _t
# multiprocessing
import multiprocessing as _mp

# configuration
from config import motor_conf as _conf

# RO-PI MOTOR
class RoPiMotor:

    # initialize
    def __init__(self, _d, _t):

	    # set PINs on BOARD
        if _conf['DEVEL_LOG'] :
            print("Initializing Motors...")
            print("> back left PIN: ", _conf['motor_back_left_pin'])
            print("> back right PIN: ", _conf['motor_back_right_pin'])
            print("> front left PIN: ", _conf['motor_front_left_pin'])
            print("> front right PIN: ", _conf['motor_front_right_pin'])
        _g.setmode(_g.BOARD)
        _g.setup(_conf['motor_back_left_pin'], _g.OUT)
        _g.setup(_conf['motor_back_right_pin'], _g.OUT)
        _g.setup(_conf['motor_front_left_pin'], _g.OUT)
        _g.setup(_conf['motor_front_right_pin'], _g.OUT)

        # directions
        self.direction1 = "f"
        self.direction2 = "f"

        # sensors
        self.distance = _d
        self.track = _t

        # queues and processes
        if _conf['DEVEL_LOG'] :
            print("Initializing Motors queues and processes...")
        self.queue1 = _mp.Queue()
        self.queue2 = _mp.Queue()
        self.process1 = _mp.Process(target=self.M1)
        self.process2 = _mp.Process(target=self.M2)
        self.process1.start()
        self.process2.start()

        if _conf['DEVEL_LOG'] : print("...init done!")

    # terminate
    def terminate(self) :
        if _conf['DEVEL_LOG'] : print("Motors termination...")
        self.cleanQueues()
        self.process1.terminate()
        self.process2.terminate()

    # activate pin
    def activate(self, p) :
        _g.output(p, _g.HIGH)

    # deactivate pin
    def deactivate(self, p) :
        _g.output(p, _g.LOW)

    # clean a queue
    def clearQueue(self, q) :
        while not q.empty() :
            q.get()

    # clean all queues
    def cleanQueues(self) :
        if _conf['DEVEL_LOG'] : print("Cleaning queues...")
        self.clearQueue(self.queue1)
        self.clearQueue(self.queue2)

    # stop motors
    def stopMotors(self) :
        self.deactivate(_conf['motor_back_left_pin'])
        self.deactivate(_conf['motor_back_right_pin'])
        self.deactivate(_conf['motor_front_left_pin'])
        self.deactivate(_conf['motor_front_right_pin'])

    # control motor process 1
    def M1(self) :
        self.worker(self.queue1, _conf['motor_back_left_pin'], _conf['motor_front_left_pin'])

    # control motor process 2
    def M2(self) :
        self.worker(self.queue2, _conf['motor_back_right_pin'], _conf['motor_front_right_pin'])

    # worker
    def worker(self, queue, backPin, frontPin) :
        while True :
            if not queue.empty() :
                direction = queue.get().split("|")
                acceleration = float(direction[1])
                direction = direction[0]
                if direction == "f" :
                    if not self.distance == False :
                        if _conf['DEVEL_LOG'] :
                            print("isClose? ", self.distance.isClose())
                        if not self.distance.isClose() :
                            self.deactivate(backPin)
                            self.activate(frontPin)
                            _t.sleep(acceleration)
                            self.deactivate(frontPin)
                    else :
                        self.deactivate(backPin)
                        self.activate(frontPin)
                        _t.sleep(acceleration)
                        self.deactivate(frontPin)
                elif direction == "b" :
                        self.deactivate(frontPin)
                        self.activate(backPin)
                        _t.sleep(acceleration)
                        self.deactivate(backPin)

    # actions
    def forward(self) :
        self.forward_duration(str(_conf['ACCELERATION_TIME']))

    def forward_duration(self, duration) :
        if not self.direction1 == "f" :
            self.clearQueue(self.queue1)
        self.direction1 = "f"
        if not self.direction2 == "f" :
            self.clearQueue(self.queue2)
        self.direction2 = "f"
        self.queue1.put("f|" + str(duration))
        self.queue2.put("f|" + str(duration))

    def backward(self) :
        self.backward_duration(str(_conf['ACCELERATION_TIME']))

    def backward_duration(self, duration) :
        if not self.direction1 == "b" :
            self.clearQueue(self.queue1)
        self.direction1 = "b"
        if not self.direction2 == "b" :
            self.clearQueue(self.queue2)
        self.direction2 = "b"
        self.queue1.put("b|" + str(duration))
        self.queue2.put("b|" + str(duration))

    def forwardleft(self) :
        self.forwardleft_duration(str(_conf['ACCELERATION_TIME']))

    def forwardleft_duration(self, duration) :
        self.clearQueue(self.queue2)
        if not self.direction1 == "f" :
            self.clearQueue(self.queue1)
        self.direction1 = "f"
        self.queue1.put("f|" + str(duration))

    def forwardright(self) :
        self.forwardright_duration(str(_conf['ACCELERATION_TIME']))

    def forwardright_duration(self, duration) :
        self.clearQueue(self.queue1)
        if not self.direction2 == "f" :
            self.clearQueue(self.queue2)
        self.direction2 = "f"
        self.queue2.put("f|" + str(duration))

    def backwardleft(self) :
        self.backwardleft_duration(str(_conf['ACCELERATION_TIME']))

    def backwardleft_duration(self, duration) :
        self.clearQueue(self.queue2)
        if not self.direction1 == "b" :
            self.clearQueue(self.queue1)
        self.direction1 = "b"
        self.queue1.put("b|" + str(duration))

    def backwardright(self) :
        self.backwardright_duration(str(_conf['ACCELERATION_TIME']))

    def backwardright_duration(self, duration) :
        self.clearQueue(self.queue1)
        if not self.direction2 == "b" :
            self.clearQueue(self.queue2)
        self.direction2 = "b"
        self.queue2.put("b|" + str(duration))

    # AUTONOMOUS GUIDE
    def autonomous(self) :
        if not self.track == False :
            self.cleanQueues()
            
            while True :
                count = 0
                if _conf['DEVEL_LOG'] : print("> searching track")
                while self.track.isOnTrack() == 0 :
                    self.forwardleft()
                    _t.sleep(_conf['AUTO_TIME'])
                    if self.track.getTrack1() == 1 :
                        if _conf['DEVEL_LOG'] : print("> found on the right")
                        self.forwardright()
                        _t.sleep(_conf['AUTO_TIME'])
                    else :
                        if _conf['DEVEL_LOG'] : print("> not found on the right")
                        self.backwardleft()
                        _t.sleep(_conf['AUTO_TIME'])
                        self.forwardright()
                        _t.sleep(_conf['AUTO_TIME'])
                        if self.track.getTrack2() == 1 :
                            if _conf['DEVEL_LOG'] : print("> found on the left")
                            self.forwardleft()
                            _t.sleep(_conf['AUTO_TIME'])
                        else :
                            count = count + 1
                            if _conf['DEVEL_LOG'] : print("> not found on the left")
                            self.backwardright()
                            _t.sleep(_conf['AUTO_TIME'])
                            if count == 5 :
                                if _conf['DEVEL_LOG'] : print("> 5 tries")
                                self.backward()
                                _t.sleep()
                                count = 0
                           
                if _conf['DEVEL_LOG'] : print("> on the line, go!")
                self.forward()
                _t.sleep(_conf['AUTO_TIME'])

        else :
            print ("Unable to use without track sensors")

# DEBUG
if __name__ == "__main__":
    print ("Welcome! Testing Motors:")
    time = 1
    wait = 3
    motor = RoPiMotor(False, False)
    motor.cleanQueues()
    print ("Forward...")
    motor.forward_duration(time)
    _t.sleep(wait)
    print ("F-Left...")
    motor.forwardleft_duration(time)
    _t.sleep(wait)
    print ("F-Right...")
    motor.forwardright_duration(time)
    _t.sleep(wait)
    print ("Backward...")
    motor.backward_duration(time)
    _t.sleep(wait)
    print ("B-Left...")
    motor.backwardleft_duration(time)
    _t.sleep(wait)
    print ("B-Right...")
    motor.backwardright_duration(time)
    _t.sleep(wait)
    print ("Goodbye!")
    motor.terminate()
    _g.cleanup()
