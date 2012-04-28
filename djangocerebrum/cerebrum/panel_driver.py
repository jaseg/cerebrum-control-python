import serial
import threading
import udpif
import pprint

FRAME_RATE = 1.0
LAMP_COUNT=26
METER_COUNT = 4
PANEL_DRIVER_PORT = "/dev/ttyACM0"

class PanelDriver:
    def __init__(self,port):
        print "INITIALIZING"
        self.sp = serial.Serial(port, 115200)
        self.fb = [1]*32
        self.te = threading.Event()
        self.lamp_count = LAMP_COUNT
        th = threading.Thread(target=self.refresh, args=(self.te, 1.0/FRAME_RATE))
        th.start()

    @classmethod
    def connect(cls, port):
        try:
            cls.driver
        except:
            print "GENERATING PANEL_DRIVER"
            cls.driver = PanelDriver(port)

    def set_lamp(self, id, val):
        print "SET LAMP", id, val
        if(val < 0):
            val*=FRAME_RATE
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
        print "Sending frame..."
        cmd = "\nb"
        for i in range(4):
            frame_data_packed = 0
            for j in range(8):
                index = i*8+j
                if self.fb[index] < 0:
                    self.fb[index]+=1
                frame_data_packed |= (0 if self.fb[index] == 0 else 1)<<j
            cmd += chr(frame_data_packed)
        cmd += "\nr\n"
        self.sp.write(cmd)
        self.sp.flush
        pprint.pprint(cmd)
        print self.sp.readline()
        print "Sent frame."

    def refresh(self, ev, interval):
        while True:
            self.send_frame()
            ev.wait(interval)
            if ev.isSet():
                break

print "FOOBAR"
PanelDriver.connect(PANEL_DRIVER_PORT)
intf = udpif.UdpInterface(PanelDriver.driver)
