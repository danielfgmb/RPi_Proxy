import requests
import json

SERVER = "194.210.159.33"


api_url = "http://"+SERVER+":8000/api/v1/apparatus/2/3/config"
response =  requests.post(api_url)
CONFIG_OF_EXP = response.json()
print(json.dumps(CONFIG_OF_EXP,indent=4))
