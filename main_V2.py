import requests
import json

SERVER = "194.210.159.33"

PORT = "8000"
FORMAT = 'utf-8'

APPARATUS_ID = "2"
EXPERIMENT_ID = "3"

CONFIG_OF_EXP = []
NEXT_EXECUTION = []
MY_IP = "192.168.1.83"
SEGREDO = "estou bem"
SAVE_DATA = []


def GetConfig():
    api_url = "http://"+SERVER+":"+PORT+"/api/v1/apparatus/"+APPARATUS_ID+"/"+EXPERIMENT_ID+"/config"
    response =  requests.post(api_url)
    CONFIG_OF_EXP = response.json()
    print(json.dumps(CONFIG_OF_EXP,indent=4))
    return ''

def GetExecution():
    api_url = "http://"+SERVER+":"+PORT+"/api/v1/getexecution/"+APPARATUS_ID
    response =  requests.get(api_url)
    NEXT_EXECUTION = response.json()
    print(json.dumps(NEXT_EXECUTION,indent=4))
    return ''

def SendPartialResult():
    api_url = "http://"+SERVER+":"+PORT+"/api/v1/sendpartialresult/"+str(NEXT_EXECUTION['execution_id'])
    todo = {"test":"ok"}
    response =  requests.post(api_url, json=todo)
    Result_id = response.json()
    print(json.dumps(Result_id,indent=4))
    return ''


if __name__ == "__main__":
    GetConfig()
    GetExecution()
    SendPartialResult()