from ctypes import ArgumentError
import RPi.GPIO as GPIO
import time
import sys
import serial
import numpy as np
import json
import pandas as pd
import configparser

import threading

from datetime import datetime


# sys.path.append('/home/pi/Cavidade/elab/webgpio/modules')
import PPT200 as PPT200


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ON = 1
OFF = 0

serial_pressure = None
Valve_cut_off = 13
Vacum_Pump=12
Discharge=5
Helio = 17
Argon = 27
Xenon = 22



def Int_GPIO():
    GPIO.setup(Valve_cut_off, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(Vacum_Pump, GPIO.OUT, initial=GPIO.HIGH)
    
    
    GPIO.setup(Helio, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(Argon, GPIO.OUT, initial=GPIO.HIGH)

    GPIO.setup(Xenon, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(Discharge, GPIO.OUT, initial=GPIO.HIGH)
    return

def Discharge_stat(ON_OFF):
    if int(ON_OFF) == 1:
        GPIO.output(Discharge, GPIO.LOW)
    elif int(ON_OFF) == 0:
        GPIO.output(Discharge, GPIO.HIGH)
    else:
        print("ERROR on the Discharge")
    return

def Vacum_Pump_stat(ON_OFF):
    if int(ON_OFF) == 1:
        GPIO.output(Vacum_Pump, GPIO.LOW)
    elif int(ON_OFF) == 0:
        GPIO.output(Vacum_Pump, GPIO.HIGH)
    else:
        print("ERROR on the Discharge")
    return

def Valve_cut_off_stat(ON_OFF):
    if int(ON_OFF) == 1:
        GPIO.output(Valve_cut_off, GPIO.LOW)
    elif int(ON_OFF) == 0:
        GPIO.output(Valve_cut_off, GPIO.HIGH)
    else:
        print("ERROR on the Discharge")
    return

def Inject_Gas(gas_type, amount):
    if gas_type == 1:
        Gas = Helio
    elif gas_type == 2:
        Gas = Argon
    elif gas_type == 3:
        Gas = Xenon
    else:
        print("ERRO: Gas selector!")
    GPIO.output(Gas, GPIO.LOW)
    time.sleep(amount*0.001)
    GPIO.output(Gas, GPIO.HIGH)
    return



#_______________ ARISNT_______________________

def int_com(COM):
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = COM
    ser.timeout = 200
    ser.open()
    print(COM)
    return  ser

def act_generator(ser):
    
    ser.write(b'gon 0\r\n')
    #print('Estou vivo 1')
    #print(ser.in_waiting)
    #print(ser.out_waiting)
    ser.flush()
    ser.flush()
    return 
    
def set_sga(ser):
    ser.write(b'sga 10000 0\r\n')
    #print(ser.in_waiting)
    #print(ser.out_waiting)
    ser.flush()
    ser.flush()
    return 'gerador activo'

def scn22(ser, strat, stop, step):
    send = b'scn22 '+ str(strat).encode('ascii')  + b' ' + str(stop).encode('ascii')  + b' ' + str(step).encode('ascii')  + b' 200 20 10700000 10000 0\r\n'
    ser.write(send)
    #print(ser.in_waiting)
    #print(ser.out_waiting)
    return 

def get_data(ser):
    data_get = b''
    ser.readline()   # read a '\n' terminated line
    ser.readline()   # read a '\n' terminated line
    ser.readline()   # read a '\n' terminated line
    ser.readline()   # read a '\n' terminated line
    ser.readline()   # read a '\n' terminated line
    ser.readline()   # read a '\n' terminated line
    
    while (True):
        line7 = ser.readline()   # read a '\n' terminated line
        data_get+=line7
        #print(line7)
        if (line7 ==b'complete\r\n'):
                break
    print('\n\r Final data: \n\r')
    print(data_get)
    
    
    return data_get


def init_saver(strat, stop, step,itera):
    size = ((stop-strat)/step)
    columns = ['Frequency [Hz]','Amp_0[dB] \n(P = ']
    save=np.zeros([int(size)+1, itera+1])
    print (size)
    data = ["" for i in range(itera)]
    
    if (itera >1):
        for i in range(1,itera):
            tag='Amp_'+str(i)+'[dB] \n(P = '
            columns.append(tag)
            
    return columns, save, data

def evalute_data(data, strat, stop, step, itera, save):
    f=strat
    for k in range(0,itera):
        t=0
        index = len(data[k])-1
        print(index)
        while (index>1):
            print(data[k][index])
            if (data[k][index] == 255):
                index -=1
                break
            index-=1
        print(index)
        for i in range(0,index,2):
            #______________Versão de testes_________________________
            #val_1 = ((data_f[i] & 0b0111)<<8)
            #val_2 = (data_f[i+1] & 0x0FF)
            #print("val_1 ") 
            #print(val_1)
            #print("val_2 ")
            #print(val_2)
            #val_f = val_1 |val_2
            #_______________________________________________________.
            val = ((data[k][i] & 0b0111)<<8) | (data[k][i+1] & 0x0FF)
            if (k==0):
                save[t][0]=f
                f=f+step
            save[t][k+1]=(80*10.0-val)/10.0  # At 25dB to -25dB
            print (save[t][k+1])
            t=t+1
    return save

def close_port(ser):
    ser.close()
    return'closed'


 

def csv_filename():
    now = datetime.now() # current date and time
    filename = now.strftime("arinst_%Y-%m-%d_%H%M%S.csv")
    print("filename :", filename)
    return filename


def upload_path():
    path = '';

    try:
        config = configparser.RawConfigParser()
        config.read('config.cfg')
        upload_dict = dict(config.items('upload'))
        path = upload_dict['path']
    except:
        print('Check config.cfg !!!')
        pass

    return path


def filename():
    return upload_path() + csv_filename()


def arnist(COM,strat, stop, step, itera):
    ser = int_com(COM)
    columns,save,data = init_saver(strat, stop, step,itera)
    #print('Estou vivo')
    #act_generator(ser)
    #set_sga(ser)
    serial_pressure = PPT200.int_com_PPT200('/dev/ttyUSB0')
    for l in range(0,itera):
        #print('Estou vivo dentro 0')
        #pressure = PPT200.get_pressure(serial_pressure)
        columns[l+1]=columns[l+1]+"{:.3f}".format(PPT200.get_pressure(serial_pressure))+ ' [mbar])'
        act_generator(ser)
        set_sga(ser)
        scn22(ser, strat, stop, step)
        #print('Estou vivo 1')
        data[l] = get_data(ser)
        #print('Estou vivo 2')
    serial_pressure.close();
    save = evalute_data(data, strat, stop, step, itera, save)
    #print('Estou vivo 3')

    df = pd.DataFrame(save, columns = columns)
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    
    # print('filename : {} '.format(filename()))

    df.to_csv(filename(), index=False)
    # json.dumps(parsed, indent=4) 
    #print('Estou vivo 4')
    
    close_port(ser)
    
    return parsed


def Do_analise_Spec(COM,strat, stop, step, itera):
    global serial_pressure
    sererial_Spec = int_com(COM)
    freq = np.arange(strat, stop, step)
    for l in range(0,itera):
        act_generator(sererial_Spec)
        set_sga(sererial_Spec)
        scn22(sererial_Spec, strat, stop, step)
        data = get_data(sererial_Spec)
        spec= evalute_data_Final(data)
        send_message = {"pressure": "{:.3f}".format(PPT200.get_pressure(serial_pressure)), "frequency": freq, "magnitude": spec  }
        print(json.dumps(send_message, indent=4))
    return
    
#data_final = arnist('COM3',3308000000, 3891000000, 500000, 4)

def evalute_data_Final(data):
    spec =[]
    index = len(data)-1
    print(index)
    while (index>1):
        print(data[index])
        if (data[index] == 255):
            index -=1
            break
        index-=1
    print(index)
    for i in range(0,index,2):
        #______________Versão de testes_________________________
        #val_1 = ((data_f[i] & 0b0111)<<8)
        #val_2 = (data_f[i+1] & 0x0FF)
        #print("val_1 ") 
        #print(val_1)
        #print("val_2 ")
        #print(val_2)
        #val_f = val_1 |val_2
        #_______________________________________________________.
        val = ((data[i] & 0b0111)<<8) | (data[i+1] & 0x0FF)
        print((80*10.0-val)/10.0 ) # At 25dB to -25dB
        spec.append((80*10.0-val)/10.0)
    return spec
    

def Set_Up_Exp(gas_select,gas_amount):
    Vacum_Pump_stat(ON)
    time.sleep(5)
    Valve_cut_off_stat(ON)
    time.sleep(50)
    # wait untly pressure is less them press_back
    Valve_cut_off_stat(OFF)
    Inject_Gas(gas_select, gas_amount)
    return


def Mauser_pressure():
    global serial_pressure
    while True:
        send_message = {"pressure": "{:.3f}".format(PPT200.get_pressure(serial_pressure))}
        print(json.dumps(send_message, indent=4))
        time.sleep(0.5)
    return



if __name__ == "__main__":
    data_thread = threading.Thread(target=Mauser_pressure,daemon=True)
    # arnist('/dev/ttyACM0', 3308000000, 3891000000, 500000, 4)
    Int_GPIO()
    serial_pressure = PPT200.int_com_PPT200('/dev/ttyUSB0')
    data_thread.start()
    # Set Up experiment:
    Set_Up_Exp(1,15)
    Do_analise_Spec('/dev/ttyACM0', 3008000000, 3391000000, 500000, 3)






# if __name__ == "__main__":
#     print("Teste functions: ")
#     Int_GPIO()
#     Discharge_stat(ON)
#     time.sleep(2)
#     Discharge_stat(OFF)
#     time.sleep(3)
#     Vacum_Pump_stat(ON)
#     time.sleep(1)
#     Vacum_Pump_stat(OFF)
#     time.sleep(2)
#     Valve_cut_off_stat(ON)
#     time.sleep(0.1)
#     Valve_cut_off_stat(OFF)
    
    
    
#     Inject_Gas(1, 6)
#     Inject_Gas(2, 5)
#     Inject_Gas(3, 1000)