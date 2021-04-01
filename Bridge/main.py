import Bridge
import Prediction
import ColorRecognition

def main():

    ser = Bridge.setup()
    while (True):
        img = Bridge.loop(ser)
        if img is not None:
            plate = Prediction.prediction(img)
            color = ColorRecognition.color_recognition()
            if plate is None:
                print("No plate found")
                Bridge.serialWrite(ser, '0')
            else:
                print(f"plate found: {plate}")
                Bridge.serialWrite(ser, '1')

if __name__ == '__main__':
    main()