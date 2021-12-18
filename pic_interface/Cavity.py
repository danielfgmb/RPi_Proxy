from ctypes import ArgumentError
import RPi.GPIO as GPIO
import time
import sys
import serial
import numpy as np
import json
import configparser

import threading

from datetime import datetime


# sys.path.append('/home/pi/Cavidade/elab/webgpio/modules')
import pic_interface.PPT200 as PPT200
import pic_interface.Arinst as Arinst
import pic_interface.GPIO as GPIO

presure = None
ON = 1
OFF = 1

def Mauser_pressure(serial_pressure):
    global pressure
    while True:
        pressure = "{:.3f}".format(PPT200.get_pressure(serial_pressure))
        send_message = {"pressure": pressure}
        print(json.dumps(send_message, indent=4))
        time.sleep(0.005)
    return



def Set_Up_Exp(gas_select,gas_amount):
    GPIO.Vacum_Pump_stat(ON)
    time.sleep(5)
    GPIO.Valve_cut_off_stat(ON)
    time.sleep(5)
    # wait untly pressure is less them press_back
    GPIO.Valve_cut_off_stat(OFF)
    GPIO.Inject_Gas(gas_select, gas_amount)
    return


def Do_analise_Spec(serial_arinst,strat, stop, step, itera):
    global pressure
    freq = np.arange(strat, stop, step)
    for l in range(0,itera):
        Arinst.act_generator(serial_arinst)
        Arinst.set_sga(serial_arinst)
        Arinst.scn22(serial_arinst, strat, stop, step)
        data = Arinst.get_data(serial_arinst)
        spec= Arinst.evalute_data_Final(data)
        # print(len(spec[1:]))
        # print(len(freq))
        # print(freq[0])
        # print(freq[-1])
        send_message = {"pressure": pressure, "frequency": freq.tolist(), "magnitude": spec[1:]  }
        print(json.dumps(send_message, indent=4))
    return
    


def Do_experiment(serial_pressure, serial_arinst,strat, stop, step, itera,back_ground,gas_pressure,gas_type):
    print("F_start: ", strat)
    print("F_end: ", stop)
    print("F_step: ", step)
    print("n_iteration: ", itera)
    print("back_pressure: ",back_ground)
    print("pressure: ",gas_pressure )
    print("gas_selector: ", gas_type)
    data_thread = threading.Thread(target=Mauser_pressure,args=(serial_pressure,),daemon=True)
    # arnist('/dev/ttyACM0', 3308000000, 3891000000, 500000, 4)
    data_thread.start()
    # Set Up experiment:
    Set_Up_Exp(gas_type,gas_pressure)
    Do_analise_Spec(serial_arinst, strat, stop, step, itera)
    time.sleep(10)