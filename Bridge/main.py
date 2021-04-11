import bridge
import prediction
import colorRecognition
import requests
import os
from google.cloud import pubsub_v1

project_id='quiet-groove-306310'
URL = 'http://127.0.0.1:5000/api/v1/activity'
#TODO: eliminare la chiave prima di caricare su cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="files/key.json"
dir_path = os.path.dirname(os.path.realpath(__file__))
model_path = f"{dir_path}\\files\\vehicle_color_haze_free_model.h5"
dev_list = []

def main():

    global dev_list

    model = colorRecognition.load(model_path)
    dev_list = bridge.setup()
    dev_list = [x for x in dev_list if x[0] is not None]

    tmp = []
    for ser, uuid in dev_list:
            subscription_name = f'{uuid}-sub'
            subscriber = pubsub_v1.SubscriberClient()
            subscription_path = subscriber.subscription_path(project_id, subscription_name)
            sub_pull = subscriber.subscribe(subscription_path, callback=callback)
            tmp.append([ser, uuid, sub_pull])
    dev_list = tmp
    print(dev_list)

    while(True):
        for ser, uuid, sub_pull in dev_list:
            try:
                sub_pull.result(timeout=1)
            except:
                pass

            ret = bridge.loop(ser, uuid)
            if ret is not None:

                img = ret[0]
                bytestream = ret[1]
                
                plate = prediction.prediction(img)
                color = colorRecognition.color_recognition(img, model)

                if plate is None:
                    print("No plate found")
                    bridge.serialWrite(ser, uuid, '0')
                else:
                    print(f"plate found: {plate}")
                    response = requests.post(URL, json={'id_gate':uuid, 'license': plate, 'color': color, 'photo': bytestream})
                    if response.status_code == 200:
                        print("Open gate")
                        bridge.serialWrite(ser, '1')
                    else:
                        print("Waiting for user's input")

def callback(message):
    uuid = message.data.decode('utf-8')
    ser = None
    for i in range(len(dev_list)):
        if dev_list[i][1] == uuid:
            ser = dev_list[i][0]
            break
    print(f"recieved message: {uuid}, {ser}")
    if ser is not None:
        bridge.serialWrite(ser, uuid, '1')
    message.ack()

if __name__ == '__main__':
    main()