import Bridge
import Prediction
import ColorRecognition

att = 5

def main():

    global att

    ser = Bridge.setup()
    while (True):
        img = Bridge.loop(ser)
        if img is not None:
            plate = Prediction.prediction(img)
            color = ColorRecognition.color_recognition(img)
            if plate is None:
                if att > 0:
                    print("No plate found")
                    Bridge.serialWrite(ser, '0')
                else:
                    print("maximum number of attempts reached")
                att -= 1
            else:
                print(f"plate found: {plate}")
                Bridge.serialWrite(ser, '1')
                att = 5

if __name__ == '__main__':
    main()