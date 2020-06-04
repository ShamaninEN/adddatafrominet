import requests
import json
# https://api.github.com/users/username/repos

my_link = 'https://api.github.com/users/shamaninen/repos'

response = requests.get(my_link)
data = response.json()
print(data)
with open('myjson.json', 'w') as f:
    json.dump(data, f)
