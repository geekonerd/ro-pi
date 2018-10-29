# GPIO
import RPi.GPIO as _g
# time utilities
import time as _t
# multiprocessing
import multiprocessing as _mp

# configuration
from config import track_conf as _conf

# RO-PI TRACKING SENSORS
class RoPiTrack:

    # initialize
    def __init__(self) :

        # set PINs on BOARD
        if _conf['DEVEL_LOG'] :
            print("Initializing Tracking...")
            print("> track 1", _conf['track_1_pin'])
            print("> track 2", _conf['track_2_pin'])
        _g.setmode(_g.BOARD)
        _g.setup( _conf['track_1_pin'], _g.IN)
        _g.setup( _conf['track_2_pin'], _g.IN)

        # set color to track, 0=black, 1=white
        self.color = _g.LOW if (_conf['color'] == 0) else _g.HIGH
        if _conf['DEVEL_LOG'] : print("> color: ", self.color)

        # track
        self.track1 = _mp.Value('i', _conf['color'])
        self.track2 = _mp.Value('i', _conf['color'])
        self.onTrack = _mp.Value('i', 0)

        # processes
        if _conf['DEVEL_LOG'] : print("Initializing processes...")
        self.process1 = _mp.Process(target=self.T1)
        self.process2 = _mp.Process(target=self.T2)
        self.process1.start()
        self.process2.start()

        if _conf['DEVEL_LOG'] : print("...init done!")

    # terminate
    def terminate(self) :
        if _conf['DEVEL_LOG'] : print("Tracking termination...")
        self.process1.terminate()
        self.process2.terminate()

    # retrieve metrics
    def isOnTrack(self) :
        if _conf['DEVEL_LOG'] : print("OnTrack? ", self.onTrack.value)
        return (int(self.track1.value) + int(self.track2.value))
    def getTrack1(self) :
        if _conf['DEVEL_LOG'] : print("Track1 value: ", self.track1.value)
        return self.track1.value
    def getTrack2(self) :
        if _conf['DEVEL_LOG'] : print("Track2 value: ", self.track2.value)
        return self.track2.value

    # tracking sensor 1
    def T1(self) :
        self.worker(_conf['track_1_pin'], self.track1)

    # tracking sensor 2
    def T2(self) :
        self.worker(_conf['track_2_pin'], self.track2)

    # worker
    def worker(self, pin, track) :
        while True :
            track.value = 0
            if _g.input(pin) == self.color :
                track.value = 1

# DEBUG
if __name__ == "__main__":
    print ("Welcome! Testing Track Sensors:")
    print ("Color #0=black, #1=white: ", _conf['color'])
    time = .3
    track = RoPiTrack()
    try:
        while True:
            print("Track1: ", track.getTrack1())
            print("Track2: ", track.getTrack2())
            print("isOnTrack: ", track.isOnTrack())
            _t.sleep(time)
    except KeyboardInterrupt:
        pass
    print ("Goodbye!")
    track.terminate()
    _g.cleanup()
