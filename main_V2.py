# import socket
import json
import requests 

interface = None


PORT = "8000"
FORMAT = 'utf-8'

SERVER = "194.210.159.33"

APPARATUS_ID = "2"
EXPERIMENT_ID ="3"

MY_IP = "192.168.1.83"
SEGREDO = "estou bem"

CONFIG_OF_EXP = []
SAVE_DATA = []



# ​/apparatus​/{apparatus_id}​/{experiment_id}​/config
def GetConfigFile():
    api_url = "http://"+SERVER+":8000/api/v1/apparatus​/2/3/config"
    print(api_url)
    # todo = {"id_RP": MY_IP, "segredo": SEGREDO}
    response =  requests.post(api_url)
    CONFIG_OF_EXP = response.json()
    print(json.dumps(CONFIG_OF_EXP,indent=4))

# def GetExperiment():
#     api_url = "http://"+SERVER+":8001/getExperiment"
#     todo = {"name":"Monte_Carlo"}
#     response =  requests.post(api_url, json=todo)
#     print (response.json())


# def SendResult():
#     api_url = "http://"+SERVER+":8001/sendResult?name="+str(NAME)
#     todo = {"msg_id":"11","data":{"val:":"1","temp":"28"}}
#     response =  requests.post(api_url, json=todo)
#     print (response.json())



if __name__ == "__main__":
    GetConfigFile()


# penso que isto devia ter um endpoint para o main server chamar quando for necessario 
# inicar a exp e a dar o status ? em vez de spamar o server com requests de 30ms em 30ms
#  