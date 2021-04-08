import requests

# BASE= "http://127.0.0.1:8080/api/v1"

# #response = requests.put(f'{BASE}/activity', json={'none':'stuff', 'userId':'franco', 'status':'ignored'}).
# #response = requests.post(f'{BASE}/gate')
# response = requests.get(f'{BASE}/login', auth=('Antonio', 'password'))
# print(response.json())
# jwt_expiry = response.json()['jwt_token_expiry']
# jwt_refresh = response.json()['jwt_token']
# # response = requests.post(f'{BASE}/gate', headers={'x-access-token':token}, json={'name':'placeholder'})
# # print(response.json())

# #response = requests.get(f'{BASE}/get', params={'jwt_refresh':jwt_refresh})
# response = requests.get(f'{BASE}/gate', headers={'x-access-token':jwt_expiry})
# print(response.json())

from storage import Storage
import io
from PIL import Image
from base64 import b64decode

client = Storage()

img = open("2.png", 'rb')
client.upload_image(img, "test5")