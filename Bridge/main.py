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

    #response = requests.put(f'{BASE}/activity', json={'none':'stuff', 'userId':'franco', 'status':'ignored'}).
    #response = requests.post(f'{BASE}/gate')
    response = requests.get(f'{BASE}/login', auth=('Antonio', 'password'))
    print(response.json())
    jwt_expiry = response.json()['jwt_token_expiry']
    jwt_refresh = response.json()['jwt_token']
    # response = requests.post(f'{BASE}/gate', headers={'x-access-token':token}, json={'name':'placeholder'})
    # print(response.json())

    #response = requests.get(f'{BASE}/get', params={'jwt_refresh':jwt_refresh})
    response = requests.get(f'{BASE}/gate', headers={'x-access-token':jwt_expiry})
    print(response.json())

if __name__ == '__main__':
    main()