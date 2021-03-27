import serial
import io
import os
from time import sleep
from PIL import Image

dir_path = os.path.dirname(os.path.realpath(__file__))
eof = b'\xff\xd9'

def setup():
    global dir_path

    # Apro il file di configurazione e leggo il parametro [PORTA]
    filename = f"{dir_path}\\files\\config.txt"
    file = open(filename, 'r')
    PORTNAME= file.readline()

    # Apro la porta seriale
    ser = serial.Serial(PORTNAME, 115200, timeout=0)
    print(f"\n{PORTNAME} port open\n")
    return ser
    

def loop(ser):
    global eof
    inbuffer=[]
    lastchar = ''
    tmp = ''
    
    # Loop infinito per ricevere i dati dalla seriale
    while(ser.in_waiting>0):     
        lastchar = ser.read(1)
        inbuffer.append(lastchar)
        if(ser.in_waiting == 0 and tmp != ""):
            tmp += lastchar
        else:
            tmp = lastchar
    if(ser.in_waiting == 0 and tmp==eof):
        tmp=""
        return useData(inbuffer, ser)

def useData(inbuffer, ser):
    global dir_path

    if(inbuffer[0] == b'\xff'):
        # Converto il mio flusso di byte in un'immagine
        print(f"Image received")
        print(f"{len(inbuffer)} bytes\n")
        bytestream = io.BytesIO(b"".join(inbuffer))
        img = Image.open(bytestream)
        # Salvo l'immagine
        img.save(f"{dir_path}\\files\\image.jpeg")
        inbuffer.clear
        return 0
    else:
        print(f"Trasmission corrupted! Sending another request...")
        inbuffer.clear
        ser.write('0'.encode())
        return None