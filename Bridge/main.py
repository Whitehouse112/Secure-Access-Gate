import Bridge
import Prediction
import ColorRecognition
import requests

uuid = "d8c0e668-b59e-455e-af78-77470ba291c5"
attempt = 5
URL = 'http://127.0.0.1:5000/api/v1/activity'

def main():

    global attempt

    ser = Bridge.setup()
    while (True):
        img = Bridge.loop(ser)
        if img is not None:
            plate = Prediction.prediction(img)
            #color = ColorRecognition.color_recognition(img)
            color = "White"
            if plate is None:
                if attempt > 0:
                    print("No plate found")
                    Bridge.serialWrite(ser, '0')
                else:
                    print("maximum number of attempts reached")
                attempt -= 1
            else:
                print(f"plate found: {plate}")
                response = requests.post(URL, json={'id_gate':uuid, 'license': plate, 'color': color})
                if response.status_code == 200:
                    print("Open gate")
                    Bridge.serialWrite(ser, '1')
                else:
                    print("Waiting for user's input")
                attempt = 5

if __name__ == '__main__':
    main()