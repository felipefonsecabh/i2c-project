from datetime import datetime
from datetime import timedelta
from smbus import SMBus
import struct
import asyncore
import socket
import threading
from multiprocessing import Process,Queue
#import socketserver

start_time = datetime.now()

def millis():
    dt = datetime.now()-start_time
    ms = (dt.days*24*60*60 + dt.seconds)*1000+dt.microseconds / 1000.0  
    return ms

#inicia escravo i2c
bus = SMBus(1) #o i2c deste rpi começa com 1
arduinoAddress = 12

#intervalo de execução
interval = 150

temperatura = 10.2
vazao = 5.3
command = 20
teste = 30

#servidor tcp assincrono

#try 1

class dataHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(500)
        #process data and send to i2c bus here
        #print(data)

class Server(asyncore.dispatcher):
    def __init__(self,host,port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.bind((host,port))
        self.listen(1)
    
    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            return
        else:
            sock,addr = pair
            print('Incoming connection from %s' %repr(addr))
            handler = dataHandler(sock)


#try 2

server = Server('localhost',8080)
loop_thread = threading.Thread(target=asyncore.loop,name="AsyncoreLoop")

if __name__ == '__main__':
    
    #try 1
    #server()

    #try 2
    loop_thread.start()
    
    prevmillis = millis()
    print('Servidor rodando')
    while True:
        currentmillis = millis()
        if(currentmillis - prevmillis > interval):
            
            
            #read i2c bus each interval
            block = bus.read_i2c_block_data(arduinoAddress,2,27)
            output = struct.unpack('6f3b',bytes(block))

            #process data
            #print(output)
            #print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

            #next execution
            prevmillis = currentmillis
        
