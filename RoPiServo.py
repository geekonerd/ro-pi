# GPIO
import RPi.GPIO as _g
# time utilities
import time as _t
# multiprocessing
import multiprocessing as _mp

# configuration
from config import servo_conf as _conf

# RO-PI SERVO SENSORS
class RoPiServo:

    # initialize
    def __init__(self):

        # set PINs on BOARD
        if _conf['DEVEL_LOG'] :
            print("Initializing Servos...")
            print("> pin 1:", _conf['servo_1_pin'])
            print("> pin 2:", _conf['servo_2_pin'])
        _g.setmode(_g.BOARD)
        _g.setup(_conf['servo_1_pin'], _g.OUT)
        _g.setup(_conf['servo_2_pin'], _g.OUT)

        # current directions
        self.angle1 = _conf['angle1']
        self.angle2 = _conf['angle2']
        self.direction1 = "u"
        self.direction2 = "l"

        # queues and processes
        if _conf['DEVEL_LOG'] : print("Initializing queues and processes...")
        self.queue1 = _mp.Queue()
        self.queue2 = _mp.Queue()
        self.process1 = _mp.Process(target=self.P1)
        self.process2 = _mp.Process(target=self.P2)
        self.process1.start()
        self.process2.start()

        if _conf['DEVEL_LOG'] : print("...init done!")

    # terminate
    def terminate(self) :
        if _conf['DEVEL_LOG'] : print("Servos termination...")
        self.clearQueue(self.queue1)
        self.clearQueue(self.queue2)
        self.process1.terminate()
        self.process2.terminate()

    # clean queue
    def clearQueue(self, q) :
        while not q.empty() :
            q.get()

    # activate pin
    def activate(self, p) :
        _g.output(p, _g.HIGH)

    # deactivate pin
    def deactivate(self, p) :
        _g.output(p, _g.LOW)

    # set and start pwm
    def startPWM(self, pin) :
        pwm = _g.PWM(pin, _conf['frequency'])
        pwm.start(0)
        return pwm

    # stop pwm
    def stopPWM(self, pwm) :
        pwm.stop()

    # set angle
    def setAngle(self, angle, pwm, pin) :
        duty = angle / 18 + 2
        self.activate(pin)
        pwm.ChangeDutyCycle(duty)
        _t.sleep(.1)
        self.deactivate(pin)
        pwm.ChangeDutyCycle(0)

    # control process 1
    def P1(self) :
        self.worker(_conf['angle1'], _conf['servo_1_pin'], self.queue1)

    # control process 2
    def P2(self) :
        self.worker(_conf['angle2'], _conf['servo_2_pin'], self.queue2)

    # worker
    def worker(self, angle, pin, queue) :
        pwm = self.startPWM(pin)
        while True :
          if not queue.empty() :
              _a = queue.get()
              if not _a == angle :
                  if not _a == 90 :
                      _a = _a + angle
                  if _a > 0 and _a < 180 :
                      angle = _a
                      self.setAngle(_a, pwm, pin)

    #actions
    def reset(self) :
        if _conf['DEVEL_LOG'] : print("reset")
        self.clearQueue(self.queue1)
        self.clearQueue(self.queue2)
        self.queue1.put(_conf['angle1'])
        self.queue2.put(_conf['angle2'])
    def up(self) :
        if _conf['DEVEL_LOG'] : print("up")
        if not self.direction1 == "u" :
            self.clearQueue(self.queue1)
        self.direction1 = "u"
        self.queue1.put(_conf['angle_backward'])
    def down(self) :
        if _conf['DEVEL_LOG'] : print("down")
        if not self.direction1 == "d" :
            self.clearQueue(self.queue1)
        self.direction1 = "d"
        self.queue1.put(_conf['angle_forward'])
    def left(self) :
        if _conf['DEVEL_LOG'] : print("left")
        if not self.direction2 == "l" :
            self.clearQueue(self.queue2)
        self.direction2 = "l"
        self.queue2.put(_conf['angle_forward'])
    def right(self) :
        if _conf['DEVEL_LOG'] : print("right")
        if not self.direction2 == "r" :
            self.clearQueue(self.queue2)
        self.direction2 = "r"
        self.queue2.put(_conf['angle_backward'])

# DEBUG
if __name__ == "__main__":
    print ("Welcome! Testing Servos:")
    time = 3
    servo = RoPiServo()
    print ("Go up 15 times...")
    for x in range(15):
        servo.up()
    _t.sleep(time)
    print ("Go left 15 times...")
    for x in range(15):
        servo.left()
    _t.sleep(time)
    print ("Go right 15 times...")
    for x in range(15):
        servo.right()
    _t.sleep(time)
    print ("Go down 15 times...")
    for x in range(15):
        servo.down()
    _t.sleep(time)
    print ("Reset...")
    servo.reset()
    _t.sleep(time)
    print ("Goodbye!")
    servo.terminate()
    _g.cleanup()
