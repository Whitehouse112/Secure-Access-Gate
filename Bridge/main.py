import Bridge
import Prediction
import ColorRecognition
import requests
from google.cloud import pubsub_v1

uuid = "d8c0e668-b59e-455e-af78-77470ba291c5"
URL = 'http://127.0.0.1:5000/api/v1/activity'
ser = None

def main():
    
    attempt = 5
    ser = Bridge.setup()

    project_id='quiet-groove-306310'
    subscription_name = f'{uuid}-sub'
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    sub_pull = subscriber.subscribe(subscription_path, callback=callback)
    
    while (True):
        
        try:
            sub_pull.result()
        except:
            sub_pull.cancel()

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
                response = requests.post(URL, json={'id_gate':uuid, 'license': plate, 'color': color})
                if response.status_code == 200:
                    print("Open gate")
                    Bridge.serialWrite(ser, '1')
                else:
                    print("Waiting for user's input")
                attempt = 5

def callback(message):
    Bridge.serialWrite(ser, '1')
    message.ack()

if __name__ == '__main__':
    main()