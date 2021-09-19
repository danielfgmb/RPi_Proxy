import requests
import json
from datetime import datetime
import importlib
import threading
import time


# SERVER = "194.210.159.33"
SERVER = "10.2.24.6"

PORT = "8000"
FORMAT = 'utf-8'

APPARATUS_ID = "2"
EXPERIMENT_ID = "3"

CONFIG_OF_EXP = []
next_execution = {}
status_config= {}
MY_IP = "192.168.1.83"
SEGREDO = "estou bem"
SAVE_DATA = []

test =True
Working = False

interface = None


def send_exp_data():
    global SAVE_DATA
    global Working
    global next_execution
    while interface.receive_data_from_exp() != "DATA_START":
        pass
    Working = True
    send_message = {"time":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"value":"","result_type":"p","status":"Experiment Starting"}
    SendPartialResult(send_message)
    while True:
        exp_data = interface.receive_data_from_exp()
        print(exp_data)
        if exp_data != "DATA_END":
            SAVE_DATA.append({"timestamp":"'+str(time.time_ns())+'","Data":exp_data})
            send_message = {"time":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"value":exp_data,"result_type":"p","status":"running"}
            SendPartialResult(send_message)
        else:
            send_message = {"time":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"value":"","result_type":"p","status":"Experiment Ended"}
            SendPartialResult(send_message)
            send_message = {"time":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"value":SAVE_DATA,"result_type":"f"}
            SendPartialResult(send_message)
            Working = False
            next_execution = {}
            return 


def Send_Config_to_Pic(myjson):
    global Working
    print("Recebi mensagem de configurestart. A tentar configurar pic")
    actual_config, config_feita_correcta = interface.do_config(myjson)
    if config_feita_correcta :   #se config feita igual a pedida? (opcional?)
        data_thread = threading.Thread(target=send_exp_data,daemon=True)
        print("PIC configurado.\n")
        if interface.do_start():                            #tentar começar experiencia
            print("aqui")
            data_thread.start()
            time.sleep(0.000001)
            #O JSON dos config parameters está mal e crasha o server. ARRANJAR
            #send_mensage = '{"reply_id": "2","status":"Experiment Running","config_params":"'+str(myjson["config_params"])+'}'
            Working = True
            send_mensage = {"reply_id": "2","status":"Experiment Running"}
        else :
            send_mensage = {"reply_id": "2", "error":"-1", "status":"Experiment could not start"}
    
    else:
        send_mensage = {"reply_id": "2", "error":"-2", "status":"Experiment could not be configured"}
    return send_mensage



# REST
def GetConfig():
    global CONFIG_OF_EXP
    api_url = "http://"+SERVER+":"+PORT+"/api/v1/apparatus/"+APPARATUS_ID+"/"+EXPERIMENT_ID+"/config"
    msg = {"secret":SEGREDO}
    response =  requests.post(api_url, json = msg)
    CONFIG_OF_EXP = response.json()
    print(json.dumps(CONFIG_OF_EXP,indent=4))
    return ''

def GetExecution():
    global next_execution
    api_url = "http://"+SERVER+":"+PORT+"/api/v1/getexecution/"+APPARATUS_ID
    response =  requests.get(api_url)
    next_execution = response.json()
    print(json.dumps(next_execution,indent=4))
    return ''

def SendPartialResult(msg):
    global next_execution
    print(next_execution)
    api_url = "http://"+SERVER+":"+PORT+"/api/v1/sendpartialresult/"+str(next_execution["execution_id"])
    # todo = {"value":{"ok":"ola","ponto":"oco"},"time":datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),"result_type":"p"}
    response =  requests.post(api_url, json=msg)
    Result_id = response.json()
    print(json.dumps(Result_id,indent=4))
    return ''


# if __name__ == "__main__":
#     GetConfig()
#     GetExecution()
#     print(json.dumps(next_execution,indent=4))
#     SendPartialResult()

def main_cycle():
    global CONFIG_OF_EXP
    global next_execution
    global status_config
    global Working
    if CONFIG_OF_EXP != None:
        if test :
            print("Esta a passar pelo if none este\n")
        while True:
            if not Working:
                if test :
                    print("Esta a passar pelo if none\n")
                GetExecution()
            if "config_params" in next_execution and not Working  :
                status_config=Send_Config_to_Pic(next_execution["config_params"])
                if test:
                    print("O valor do Working é: "+str(Working))
            # pass
            # print("teste 12")
            # print(Working)

    return ''

if __name__ == "__main__":
    print("[Starting] Experiment Server Starting...")
    # global next_execution
    connected = None
    interface = importlib.import_module("pic_interface.interface")
    while True:
        # try:
        GetConfig()
        if interface.do_init(CONFIG_OF_EXP) :
            main_cycle()
        else:
            print ("Experiment not found")
        # except:
        #     #LOG ERROR
        #     print("Faill to connect to the Server. Trying again after 10 s")
        #     #So faz shutdown do socket se este chegou a estar connected
        #     time.sleep(10)



# global CONFIG_OF_EXP
# global interface
# interface = importlib.import_module("pic_interface.interface")
# print("Recebi mensagem de configuracao. A tentar inicializar a experiencia\n")
# CONFIG_OF_EXP = myjson['config_file']

# #LIGAR A DISPOSITIVO EXP - INIT
# #Talvez passar erros em forma de string JSON para incluir no reply em vez de OK e NOT OK
# if interface.do_init(CONFIG_OF_EXP) :
#     send('{"reply_id": "1", "status":"Experiment initialized OK"}')

# else :
#     send('{"reply_id": "1", "error":"-1", "status":"Experiment initialized NOT OK"}')