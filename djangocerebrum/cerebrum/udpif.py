from scapy.all import *
#from functools import partial
import threading

class UdpInterface(threading.Thread):
    def __init__(self, driver, start_port=32768, blink_duration=0.5):
        super(UdpInterface, self).__init__()
        self.driver, self.start_port, self.blink_duration = driver, start_port, blink_duration
        self.start()

    def run(self):
        print "Starting to sniff"
        sniff(prn=self.recv_pkt)

    def recv_pkt(self, pkt):
        if UDP in pkt and pkt[UDP].dport in range(self.start_port, self.start_port+self.driver.lamp_count):
            self.driver.set_lamp(pkt[UDP].dport - self.start_port, -self.blink_duration)
