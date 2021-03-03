import requests

BASE= "http://127.0.0.1:8080/api/v1"

response = requests.post(f'{BASE}/gate', data={'none':'stuff'})
print(response)