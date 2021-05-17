from pyfcm import FCMNotification

DEVICE_TOKEN = "cYgzqik3Sdu88GhM6Kz7FO:APA91bFyrSyqmoM0KoTRkZAxaESVfKOPwttewVuIzFsj_5XyZyWmDLT5Uksi-ert1M4IlMZWK4BPHJyy1azbTkkDHLlhpvuzGhDRP8rZqlX9XaKYdXm3JsAS7LDdDM62T-5CymXw_OHf"

token = "dc89bX3hSJuPeSmMlzgDf_:APA91bFjQoOhz-zIhc-3Tdy84at2yUyqMoMGvGtJ8ea9IgJMqWE9YRgJN5-a1O5aClP4YH5W5LVX3b76EUXq85bhfbNJBUkPoAHu7y1UApTaGEJrSr2JJsLaKG_Iv9jFfDuz_xDlXFnQ"
title = "Tentativo di accesso rilevato"
body = f"Una macchina è stata rilevata al cancello 'My Home'"
data = {"id_gate":"e9e59c2c-28d9-4748-9ec5-df524f25cc94", "type":"anomaly"}

push_service = FCMNotification(api_key="AAAAxL7lTsI:APA91bEsVnNzbVM2cZ2rbkl05xSYf7IVMayZpszta2QiCCqgP-8TvtDMzvkQLuQxPJuAlApXRLQQJMsBzH2a7hg9FTboUMNtAmDQktvdjp-_LNk7x7NfzsiE71ETxSd1OknVmlexum3h")
push_service.notify_single_device(token, message_title=title, message_body=body, data_message=data)