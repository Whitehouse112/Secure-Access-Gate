import Bridge
import Prediction
import ColorRecognition

uuid = "d8c0e668-b59e-455e-af78-77470ba291c5"
attempt = 5

def main():

    global attempt

    ser = Bridge.setup()
    while (True):
        img = Bridge.loop(ser)
        if img is not None:
            plate = Prediction.prediction(img)
            color = ColorRecognition.color_recognition(img)
            if plate is None:
                if attempt > 0:
                    print("No plate found")
                    Bridge.serialWrite(ser, '0')
                else:
                    print("maximum number of attempts reached")
                attempt -= 1
            else:
                print(f"plate found: {plate}")
                #controllare che non ci siano anomalie
                Bridge.serialWrite(ser, '1')
                attempt = 5

if __name__ == '__main__':
    main()