#!usr/bin/env python
import socket
from datetime import datetime
from datetime import timedelta

start_time = datetime.now()

def millis():
    dt = datetime.now()-start_time
    ms = (dt.days*24*60*60 + dt.seconds)*1000+dt.microseconds / 1000.0  
    return ms

class Client():
   def __init__(self,Adress=("127.0.0.1",8080)):
      self.s = socket.socket()
      self.s.connect(Adress)

testjson = '{"temps":[5,10,15,20],"flows":[20,10],"status":[0,0,0],"malha_vq":[2,5,102],"malha_vf":[3,11,52]}\n'
c = Client()
prevmillis = millis()

if __name__=='__main__':
    while True:
        currentmillis = millis()
        if currentmillis - prevmillis > 1500 :
            c.s.sendall(testjson.encode('utf-8')) #python3
            prevmillis = currentmillis