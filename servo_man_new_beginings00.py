# BY: m3ch-l0rd
# DATE: 05102026'ish
#-----------------------------------------
# new project / servoMan begginer baseline
#-----------------------------------------
# The Official "new Beginning" for v0.3.5
#
# Features:
# - 3 servo's
# - 5 leds (not counting on board)
# rpi pico on board items:
# - board temp
# - vRef read
# adafruit parts pal kit components:
# - photocell basic light detection 
# - 5v power supply regulation 
# - on/off switch 

import machine
from machine import Pin, PWM
import utime
import random

#HEAD

    #EYES
er1 = Pin(6, machine.Pin.PULL_DOWN)
er2 = Pin(7, machine.Pin.PULL_DOWN)

#er3 = PWM(Pin(6,7)) 
#er3.freq(500)
#duty = 0
#direction = 1

    #MOUTH
mg1 = Pin(9, machine.Pin.PULL_DOWN)
mg2 = Pin(10, machine.Pin.PULL_DOWN)
mg3 = Pin(11, machine.Pin.PULL_DOWN)

#on board
led = Pin(25,Pin.OUT)

#voltage Check
adc = machine.ADC(0)
vdc = adc.read_u16()
voltage = vdc * (3.3 / 65535)
# print(voltage)

#boardTemp
onBoardTemp = machine.ADC(4)
volt = (3.3/65535) * onBoardTemp.read_u16()
temp = 27 - (volt - 0.706)/0.01721

#cds photo resistor
dark = Pin(1, machine.Pin.PULL_UP)

#PWM Values 
OFF = 0000000
MID = 1500000
MIN = 1000000
MAX = 2000000
hYp = 2500000
BUZ = 1000000
# {previously was using 7 digit pwm values. (2500 is 90*). **went back and forth between running 4 and 7 digit pwm values.
# i think it likes 7}


buz = PWM(Pin(15))
buz.freq(550)
buz.duty_ns(OFF)

pwm = PWM(Pin(0)) # left arm 
pwm.freq(50)
pwm.duty_ns(MID) # ---- ----  S E R V O ' S 


pwm_2 = PWM(Pin(20)) #right arm
pwm_2.freq(50)
pwm_2.duty_ns(MID) # ---- -- A R E - A L L - S E T 

pwm_3 = PWM(Pin(21)) #head
pwm_3.freq(50)
pwm_3.duty_ns(MID) # ---- -- T O - M I D - O N - S T A R T 

# ---------- F U N C T I O N S ----------!! 

def boardTemp():
    print(round(temp, 1))

def head_movement_diagnostic(): #{CHECK - COMPLETE; MOVES HEAD}
    pwm_3.duty_ns(MIN)
    utime.sleep(.5)
    pwm_3.duty_ns(MAX)
    utime.sleep(.5)
    pwm_3.duty_ns(MID)
    print("head_movement_diagnostic complete")    


    
def power_on_blink(): #{CHECK - COMPLETE; FLASHES BOARD LED}   
    led.toggle()
    utime.sleep(.5)
    led.toggle()
    utime.sleep(.5)
    led.toggle()
    
    
    
    
    #eyes
def eyes_sequence():#{CHECK - COMPLETE; TURNS EYES OFF/ON}
    er1.toggle()
    er2.toggle()
    utime.sleep(1)
    er1.toggle()
    er2.toggle()
    utime.sleep(1)
    er1.toggle()
    er2.toggle()
    print("eyes_sequence complete")

def mouth_sequence():
    mg1.value(0)
    mg2.value(0)
    mg3.value(0)
    utime.sleep(.5)
    mg2.value(1)
    utime.sleep(0.5)
    mg2.value(0)
    print("mouth_sequence complete")
    
def buzzer_test():
    buz.duty_ns(BUZ)
    utime.sleep(1)
    buz.duty_ns(OFF)
    utime.sleep(1)
    buz.duty_ns(BUZ)
    utime.sleep(1)
    buz.duty_ns(OFF)
    #utime.sleep(0.20)
    #buz.duty_ns(OFF)
    #utime.sleep(0.20)
    print("buzzer_test complete")

    #MOUTH
def mouth_led_sequence(): #{ NEEDS WORK - INCORRECTLY MAPED , NO PIEZO}
    mg1.value(0) #left corner of mouth
    utime.sleep(1)
    mg2.value(0) #right corner of mouth
    utime.sleep(1)
    mg3.value(0) #mouth center
    utime.sleep(1) 
    # piezo 
    buz.duty_ns(MIN)
    utime.sleep(1)
    buz.duty_ns(OFF)
    mg2.value(1) #mouth center
    utime.sleep(1)
    buz.duty_ns(MIN)
    mg2.value(0)
    utime.sleep(1)
    mg2.value(1)
    buz.duty_ns(OFF)
    utime.sleep(1)
    mg2.value(0)
    buz.duty_ns(MIN)
    utime.sleep(1)
    mg2.value(1)
    buz.duty_ns(OFF)
    utime.sleep(1)
    mg2.value(0)
    buz.duty_ns(MIN)
    utime.sleep(1)
    buz.duty_ns(OFF)
    print("talking buz seq complete")
    
    #arm servo sequence_00
def arm_ss_a():
    pwm.duty_ns(MID)
    pwm_2.duty_ns(MID)
    utime.sleep(1)
    pwm.duty_ns(MAX)
    pwm_2.duty_ns(MAX)
    utime.sleep(1)
    pwm.duty_ns(MID)
    pwm_2.duty_ns(MID)
    utime.sleep(1)
    print("arm_ss_a complete")
    
    #arm servo sequence_01
def arm_ss_b():
    print('servo sequence_01')
    pwm.duty_ns(MID)				#pwm is left arm & reversed MIN is MAX (forward)
    pwm_2.duty_ns(MID)
    utime.sleep(.5)
    pwm.duty_ns(MIN)
    utime.sleep(.5)
    pwm.duty_ns(MID)
    utime.sleep(.5)
    pwm.duty_ns(MIN)
    utime.sleep(.5)
    pwm.duty_ns(MID)
    utime.sleep(.5)
    print('servo sequence_01 END')
    
    #double eye blink
def eye_blink():
    er1.toggle()
    er2.toggle()
    utime.sleep(.25)
    er1.toggle()
    er2.toggle()
    utime.sleep(.25)
    er1.toggle()
    er2.toggle()
    utime.sleep(.25)
    er1.toggle()
    er2.toggle()
    utime.sleep(.25)
    print("eye_blink complete")   
    #arm servo sequence_02
def arm_ss_c():
    pwm.duty_ns(MAX)
    pwm_2.duty_ns(MAX)
    utime.sleep(.25)
    pwm.duty_ns(MID)
    pwm_2.duty_ns(MID)
    utime.sleep(.25)
    pwm.duty_ns(MIN)
    pwm_2.duty_ns(MIN)
    utime.sleep(.25)
    pwm.duty_ns(MAX)
    pwm_2.duty_ns(MAX)
    utime.sleep(.25)
    pwm.duty_ns(MID)
    pwm_2.duty_ns(MID)
    utime.sleep(.25)
    pwm.duty_ns(MIN)
    pwm_2.duty_ns(MIN)
    utime.sleep(1)
    print("end servo sequence c")
    
    
    #arm_servo_sequence 03
def arm_ss_d():
    pwm.duty_ns(MID)
    pwm_2.duty_ns(MID)
    utime.sleep(.25)
    #pwm.duty_ns(hYp)
    pwm_2.duty_ns(hYp)
    utime.sleep(.5)
    
    #eye fade
def eyes_led_a(): #{ NEEDS WORK - FADE FUNCTION FAILED}
    for _ in range(8* 256):
        duty_ns += direction
        if duty_ns > 255:
            duty = 255
            direction = -1
        elif duty < 0:				#attempting to fade the eyes this worked but it does each eye one at a time 
            duty = 0
            direction = 1
        er3.duty_u16(duty * duty)
        utime.sleep(0.001)
        
def hybernate():
    print("going to sleep now")
    utime.sleep(50)
    print("hybernation sleep complete")
    
def zombieMode():
    pwm.duty_ns(MAX)
    pwm_2.duty_ns(MIN)
    utime.sleep(1)
    pwm.duty_ns(MID)
    pwm_2.duty_ns(MID)
    utime.sleep(1)
    pwm.duty_ns(MAX)
    pwm_2.duty_ns(MIN)
    utime.sleep(1)
    pwm.duty_ns(MID)
    pwm_2.duty_ns(MID)
    utime.sleep(1)    
    print("zombieMode done")
    
def runningFace():
    for i in range(3):    
        er1.value(1)
        er2.value(1)
        utime.sleep(0.5)
        mg1.value(1)
        mg2.value(1)
        mg3.value(1)
        utime.sleep(1)
        mg2.toggle()
        utime.sleep(0.2)
        mg2.toggle()
        mg3.toggle()
        utime.sleep(0.2)
        mg3.toggle()
        er2.toggle()
        utime.sleep(0.2)
        er2.toggle()
        er1.toggle()
        utime.sleep(0.2)
        er1.toggle()
        mg1.toggle()
        utime.sleep(0.2)
        mg1.toggle()
        mg2.toggle()
        utime.sleep(0.2)
        mg2.toggle()
        mg3.toggle()
        utime.sleep(0.2)
        mg3.toggle()
        er2.toggle()
        utime.sleep(0.2)
        er2.toggle()
        er1.toggle()
        utime.sleep(0.2)
        er1.toggle()
        mg1.toggle()
        utime.sleep(0.2)
        mg1.toggle()
        mg2.toggle()
        utime.sleep(0.2)
        mg2.toggle()
    print("runningFace ran.")
    print("Temp *C: ", temp)
    print("Current VDC: ", voltage)
  
# Put the function names directly in the list (no parentheses)
functions = [runningFace, eyes_sequence, mouth_sequence, zombieMode, arm_ss_a, arm_ss_b, arm_ss_c, eye_blink, mouth_led_sequence, hybernate, buzzer_test]
lightsOnly = [runningFace, eyes_sequence, mouth_sequence, eye_blink, mouth_led_sequence, hybernate, buzzer_test]

# ********************** l00p *********************
# you can comment everything out below
# and run individual functions in the repl by name
# to test and develop specific functions

while True:
    runRandom = random.choice(lightsOnly) # Function sequences will be randomly chose from the array named in the parenthesis
                                          # lights only is selected by default so there is no chance of a servo movement interfering with
                                          # power or data cables.
                                          # if you are ready to run random functions with servos
                                          # cables and wires manages, save to main.py and unplug the usb. 
    
    # Run the function that was picked
    runRandom()
    
    # Pause so it doesn't run at light speed
    utime.sleep(1)
    #print(voltage)
    
    
 