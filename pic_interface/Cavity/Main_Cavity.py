from ctypes import ArgumentError
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ON = 1
OFF = 0

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


if __name__ == "__main__":
    print("Teste functions: ")
    Int_GPIO()
    Discharge_stat(ON)
    time.sleep(2)
    Discharge_stat(OFF)
    time.sleep(3)
    Vacum_Pump_stat(ON)
    time.sleep(1)
    Vacum_Pump_stat(OFF)
    time.sleep(2)
    Valve_cut_off_stat(ON)
    time.sleep(10)
    Valve_cut_off_stat(OFF)
    
    
    
    Inject_Gas(1, 5)
    Inject_Gas(2, 5)
    Inject_Gas(3, 1000)