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
    time.sleep(10)
    # wait untly pressure is less them press_back
    GPIO.Valve_cut_off_stat(OFF)
    GPIO.Inject_Gas(gas_select, gas_amount)
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
    Arinst.Do_analise_Spec(serial_arinst, strat, stop, step, itera)
    time.sleep(10)