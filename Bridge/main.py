import Bridge
import Prediction

def main():

    ser = Bridge.setup()
    while (True):
        img = Bridge.loop(ser)
        if img is not None:
            plate = Prediction.detection(img)
            if plate is None:
                print("No plate found")
                Bridge.serialWrite(ser, '0')
            else:
                print(f"plate found: {plate}")

if __name__ == '__main__':
    main()