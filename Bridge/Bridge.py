import serial
import urllib.request
import io
import os
from time import sleep
from PIL import Image

## configuration
PORTNAME='COM4'
eof=b'\xff\xd9'

class Bridge():

    def setup(self):
        # open serial port in
        self.ser = serial.Serial(PORTNAME, 115200, timeout=0)
        print(f"\n{PORTNAME} port open\n")
        self.inbuffer=[]
        self.lastchar = ''

    def loop(self):
        tmp = ''
       
        # infinite loop to receive data
        while (True):
            while(self.ser.in_waiting>0):     
                self.lastchar = self.ser.read(1)
                self.inbuffer.append(self.lastchar)
                if(self.ser.in_waiting == 0 and tmp != ""):
                    tmp += self.lastchar
                else:
                    tmp = self.lastchar
            if(self.ser.in_waiting == 0 and tmp==eof):
                tmp=""
                self.useData()

    def useData(self):
        if(self.inbuffer[0] == b'\xff'):
            print(f"Image received")
            print(f"{len(self.inbuffer)} bytes\n")
            bytestream = io.BytesIO(b"".join(self.inbuffer))
            #Show image
            img = Image.open(bytestream)
            img.show()
            #Save image
            dir_path = os.path.dirname(os.path.realpath(__file__))
            img.save(f"{dir_path}\\photos\\{len(self.inbuffer)}.jpeg")
            self.inbuffer = []
        else:
            print(f"Trasmission corrupted! Sending another request...")
            self.inbuffer.clear
            sleep(3)
            self.ser.write('0'.encode())

    def saveData(self):
        #save byte
        f_b = open("byte.txt", "a+")
        f_b.write(f"\n\n------------- UXGA 10 {len(self.inbuffer)}-------------\n")
        f_b.write((str)(b"".join(self.inbuffer)))
        f_b.close()
        #convert byte to int and save
        f_i = open("integer.txt", "a+")
        f_i.write(f"\n\n------------- UXGA 10 {len(self.inbuffer)}-------------\n")
        integer = [int.from_bytes(x, "big") for x in self.inbuffer]
        f_i.write("".join((str)(integer)))
        f_i.close()

if __name__ == '__main__':
    br=Bridge()
    br.setup()
    br.loop()