import requests
import json
my_link = 'https://hst-api.wialon.com/wialon/ajax.html'
token = '004b0af066bb9523aa365b884ba690d7774356568392DEFC497E2179C27C5300D6E8EA1B'
my_params = {
    "token":token,
    "fl":8
}
to_json_params = json.dumps(my_params)
params = {
    "svc": "token/login",
    "params":to_json_params
}
response = requests.get(my_link, params=params)
data = response.json()
print(data)
with open('my_wialon.json', 'w') as f:
    json.dump(data, f)