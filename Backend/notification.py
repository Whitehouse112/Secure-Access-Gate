from pyfcm import FCMNotification

DEVICE_TOKEN = "cYgzqik3Sdu88GhM6Kz7FO:APA91bFyrSyqmoM0KoTRkZAxaESVfKOPwttewVuIzFsj_5XyZyWmDLT5Uksi-ert1M4IlMZWK4BPHJyy1azbTkkDHLlhpvuzGhDRP8rZqlX9XaKYdXm3JsAS7LDdDM62T-5CymXw_OHf"

class Notification:
    def __init__(self):
        #TODO: cambiare api_key con una generata nel progetto cloud
        self.push_service = FCMNotification(api_key="AAAAxL7lTsI:APA91bEsVnNzbVM2cZ2rbkl05xSYf7IVMayZpszta2QiCCqgP-8TvtDMzvkQLuQxPJuAlApXRLQQJMsBzH2a7hg9FTboUMNtAmDQktvdjp-_LNk7x7NfzsiE71ETxSd1OknVmlexum3h")

    def sendToTopic(self, topic, title, body):

        self.push_service.notify_topic_subscribers(topic, message_title=title, message_body=body)

    def sendToDevice(self, token, title, body, data):

        self.push_service.notify_single_device(token, message_title=title, message_body=body, data_message=data)