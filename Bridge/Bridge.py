import serial
import io
import os
from serial.tools import list_ports
from time import sleep
from PIL import Image
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
eof = b'\xff\xd9'
inbuffer = []

def setup():

    ports_list = []
    coms = [y.name for y in list_ports.comports() if 'Bluetooth' in y.description and "_C00000000" in y.hwid]
    coms.sort()

    for portname in coms:
        try:
            # Apro la porta seriale
            ser = serial.Serial(portname, 115200, timeout=0)
            print(f"{portname} port open")
            ports_list.append(ser)
        except Exception as e:
            print(f"Error while opening {portname}")
            ports_list.append(None)
        
    # Apro il file di configurazione e leggo gli uuid dei sensori
    filename = f"{dir_path}\\files\\config.txt"
    file = open(filename, 'r')
    uuid_list = file.readlines()
    uuid_list = [x.replace('\n', "") for x in uuid_list]
    file.close()

    print("Done")
    return [[ports_list[x], uuid_list[x]] for x in range(len(ports_list))]

def loop(ser, uuid):
    
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
        return useData(ser, uuid)

    inbuffer.clear()
    return None

def useData(ser, uuid):

    if(inbuffer[0] == b'\xff'):
        # Converto il mio flusso di byte in un'immagine
        print(f"Image received from sensor {uuid}")
        print(f"{len(inbuffer)} bytes\n")
        bytestream = io.BytesIO(b"".join(inbuffer))
        img = Image.open(bytestream)

        # Salvo l'immagine
        img.save(f"{dir_path}\\files\\{uuid}-image.jpeg")
        inbuffer.clear()

        # Converto l'immagine in formato openCV
        return [np.array(img), bytestream]
    else:
        return serialWrite(ser, uuid, '0')


def serialWrite(ser, uuid, code):
    
    if code == '0':
        print(f"Something went wrong in sensor {uuid}...sending another request\n")
        inbuffer.clear()
        ser.write(code.encode())

    if code == '1':
        print(f"Opening gate {uuid}...\n")
        ser.write(code.encode())
    
    return None