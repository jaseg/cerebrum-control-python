import serial
import threading

FRAME_RATE = 20.0
LAMP_COUNT=26
METER_COUNT = 4
PANEL_DRIVER_PORT = "/dev/arduino1"

class PanelDriver:
    def __init__(self,port):
        self.sp = serial.Serial(port, 57600)
        self.fb = [0]*32
        self.te = threading.Event()
        th = threading.Thread(target=self.refresh, args=(self.te, 1.0/FRAME_RATE))
        print "WE ARE ALL GOING TO DIE!!1!"
        th.start()

    @classmethod
    def connect(cls, port):
        try:
            cls.driver
        except:
            cls.driver = PanelDriver(port)

    def set_lamp(self, id, val):
        print "SET LAMP", id, val
        self.fb[int(id)] = int(val)
        return val
    
    def get_lamp(self, id):
        print "GET LAMP", id
        return self.fb[int(id)]

    def set_meter(self, id, val): #TODO
        pass

    def get_meter(self, id): #TODO
        pass

    def send_frame(self):
        self.sp.write('b')
        for i in range(4):
            frame_data_packed = 0
            for j in range(8):
                index = i*8+j
                if self.fb[index] < 0:
                    self.fb[index]+=1
                frame_data_packed |= (0 if self.fb[index] == 0 else 1)<<j
            self.sp.write(chr(frame_data_packed))
        self.sp.flush

    def refresh(self, ev, interval):
        while True:
            self.send_frame()
            ev.wait(interval)
            if ev.isSet():
                break

print "FOOBAR"
PanelDriver.connect(PANEL_DRIVER_PORT)
