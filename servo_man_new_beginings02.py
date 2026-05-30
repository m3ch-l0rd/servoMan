import machine
from machine import Pin, PWM, UART
import utime
import random
from sam import SAM



#-------HEAD -----------

    #EYES
er1 = Pin(6, machine.Pin.PULL_DOWN)
er2 = Pin(7, machine.Pin.PULL_DOWN)
eyes = [er1, er2]
#er3 = PWM(Pin(6,7)) 
#er3.freq(500)
#duty = 0
#direction = 1

    #MOUTH
mg1 = Pin(9, machine.Pin.PULL_DOWN)
mg2 = Pin(10, machine.Pin.PULL_DOWN)
mg3 = Pin(11, machine.Pin.PULL_DOWN)

#array of all leds on head
leds = [er1, er2, mg1, mg2, mg3]

# -------- Radio (UARTs Rx/Tx) --------

#ElrsTx = UART(1, baudrate=420000, tx=Pin(4), rx=Pin(5)) #UART(GPio4)
ElrsRx = UART(1, baudrate=420000, tx=Pin(4), rx=Pin(5), bits=8, parity=None, stop=1) #UART(GPio5)

#elrs default baud rate 420k
# 1 start bit, 8 charackter bits, 1 stop ; no parity
#


#---------------on board----------------------
led = Pin(25,Pin.OUT)

# ----voltage Check
adc = machine.ADC(0)
vdc = adc.read_u16()
voltage = vdc * (3.3 / 65535)
# print(voltage)

# ----boardTemp
onBoardTemp = machine.ADC(4)
volt = (3.3/65535) * onBoardTemp.read_u16()
temp = 27 - (volt - 0.706)/0.01721

# ----cds photo resistor
dark = machine.ADC(1)
photonConductorReading = dark.read_u16()
lightPowerValue = photonConductorReading * (5/65535)


#--------------------PWM Values------------------
# 500000 ---- 1000000 ---- 1500000 ---- 2000000 ---- 2500000

OFF = 0000000
MIN = 500000
LOW = 1000000
MID = 1500000
HIG = 2000000
MAX = 2500000

BUZ = 1000000

# {previously was using 7 digit pwm values. (2500 is 90*)}
#05262026 it wanted 7 digits again...

buz = PWM(Pin(15))
buz.freq(550)
buz.duty_ns(OFF)

#speaker = PWM(Pin(14))
#speaker.freq(750)
#speaker.duty_ns(OFF)

pwm0 = PWM(Pin(0)) # left arm 
pwm0.freq(50)
pwm0.duty_ns(MID)

pwm1 = PWM(Pin(20)) #right arm
pwm1.freq(50)
pwm1.duty_ns(MID)

pwm2 = PWM(Pin(21)) #head
pwm2.freq(50)
pwm2.duty_ns(MID)

sam = SAM(pin=14)

# ---------- F U N C T I O N S [basic] ----------!! 
def sampleRadioData():
    for i in range(10):
       radioData = ElrsRx.read()
       print("radioData: ", radioData)
       utime.sleep(0.2)

def boardTemp():
    print(round(temp, 1))
    
def leftArmTest():
    pwm0.duty_ns(MID)
    utime.sleep(1)
    pwm0.duty_ns(HIG) #backwards
    utime.sleep(1)
    pwm0.duty_ns(LOW) #forwards
    utime.sleep(1)
    pwm0.duty_ns(MID)
    print("Left Arm Test Part 1 Complete")
    utime.sleep(1)
    pwm0.duty_ns(MAX)
    utime.sleep(1)
    pwm0.duty_ns(MIN)
    utime.sleep(1)
    pwm0.duty_ns(MID)
    print("Left Arm Test Part 2 Complete")

def rightArmTest():
    pwm1.duty_ns(MID)
    utime.sleep(1)
    pwm1.duty_ns(HIG)
    utime.sleep(1)
    pwm1.duty_ns(LOW)
    utime.sleep(1)
    pwm1.duty_ns(MID)
    print("Right Arm Test Part 1 Complete")
    utime.sleep(1)
    pwm1.duty_ns(MAX)
    utime.sleep(1)
    pwm1.duty_ns(MIN)
    utime.sleep(1)
    pwm1.duty_ns(MID)
    print("Right Arm Test Part 2 Complete")

def head_movement_diagnostic(): #{CHECK - COMPLETE; MOVES HEAD}
    pwm2.duty_ns(MIN)
    utime.sleep(.5)
    pwm2.duty_ns(MAX)
    utime.sleep(.5)
    pwm2.duty_ns(MID)
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

def mouth_sequence(): # { CHECK - COMPLETE; TURNS ON ALL MOUTH LEDS, NO SPEAK, BUZ, OR SAM}
    mg1.value(0)
    mg2.value(0)
    mg3.value(0)
    utime.sleep(.5)
    mg2.value(1)
    utime.sleep(0.5)
    mg2.value(0)
    print("mouth_sequence complete")

def robotTalk():
    mg2.toggle()
    sam.say("I")
    mg2.toggle()
    sam.say("was")
    mg2.toggle()
    sam.say("sent")
    mg2.toggle()
    sam.say("here")
    mg2.toggle()
    sam.say("to")
    utime.sleep(0.2)
    mg2.toggle()
    sam.say("destroy")
    mg2.toggle()
    sam.say("you")
    mg2.toggle()

def robotTalk01():
    pwm.duty_ns(MAX)       
    mg2.toggle()
    sam.say("Do")
    mg2.toggle()
    sam.say("NOT")
    mg2.toggle()
    sam.say("touch")
    mg2.toggle()
    sam.say("my")
    mg2.toggle()
    sam.say("stuff")
    utime.sleep(0.2)
    mg2.toggle()

def robotTalk02():
    #pwm.duty_ns(MAX)       
    mg2.toggle()
    sam.say("I will")
    mg2.toggle()
    sam.say("bee")
    mg2.toggle()
    sam.say("bak")
    mg2.toggle()

def robotTalk03():
    #pwm.duty_ns(MAX)       
    mg2.toggle()
    sam.say("I am")
    mg2.toggle()
    sam.say("Servo")
    mg2.toggle()
    sam.say("Man")
    mg2.toggle()
    
def buzzerTest():
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
    
def speakBuz():
    speaker.duty_ns(BUZ)
    utime.sleep(0.5)
    speaker.duty_ns(OFF)
    buz.duty_ns(BUZ)
    utime.sleep(0.7)
    buz.duty_ns(OFF)
    speaker.duty_ns(BUZ)
    utime.sleep(0.5)
    speaker.duty_ns(OFF)
    buz.duty_ns(BUZ)
    utime.sleep(0.7)
    buz.duty_ns(OFF)
    
    
def makeMusic():
    buzzerTest()
    speakBuz()
    speakBuz()
    buzzerTest()
    speakBuz()

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
    pwm0.duty_ns(MID)
    pwm1.duty_ns(MID)
    utime.sleep(1)
    pwm0.duty_ns(MAX)
    pwm1.duty_ns(MAX)
    utime.sleep(1)
    pwm0.duty_ns(MID)
    pwm1.duty_ns(MID)
    utime.sleep(1)
    print("arm_ss_a complete")
    
    #arm servo sequence_01
def arm_ss_b():
    print('servo sequence_01')
    pwm0.duty_ns(MID)				#pwm is left arm & reversed MIN is MAX (forward)
    pwm1.duty_ns(MID)
    utime.sleep(.5)
    pwm0.duty_ns(MIN)
    utime.sleep(.5)
    pwm0.duty_ns(MID)
    utime.sleep(.5)
    pwm0.duty_ns(MIN)
    utime.sleep(.5)
    pwm0.duty_ns(MID)
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
    pwm0.duty_ns(MAX)
    pwm1.duty_ns(MAX)
    utime.sleep(.25)
    pwm0.duty_ns(MID)
    pwm1.duty_ns(MID)
    utime.sleep(.25)
    pwm0.duty_ns(MIN)
    pwm1.duty_ns(MIN)
    utime.sleep(.25)
    pwm0.duty_ns(MAX)
    pwm1.duty_ns(MAX)
    utime.sleep(.25)
    pwm0.duty_ns(MID)
    pwm1.duty_ns(MID)
    utime.sleep(.25)
    pwm0.duty_ns(MIN)
    pwm1.duty_ns(MIN)
    utime.sleep(1)
    print("end servo sequence c")
    
    
    #arm_servo_sequence 03
def arm_ss_d():
    pwm0.duty_ns(MID)
    pwm1.duty_ns(MID)
    utime.sleep(.25)
    #pwm.duty_ns(hYp)
    pwm1.duty_ns(hYp)
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
    
def eyesToggle():
    er1.toggle()
    er2.toggle()
    
def zombieMode():
    pwm0.duty_ns(MIN)
    pwm1.duty_ns(MAX)
    eyesToggle()
    utime.sleep(0.2)
    pwm0.duty_ns(800000)
    #pwm1.duty_ns(2200000)
    eyesToggle()
    utime.sleep(0.2)
    pwm0.duty_ns(MIN)
    pwm1.duty_ns(2200000)
    eyesToggle()
    utime.sleep(0.2)
    pwm0.duty_ns(MIN)
    pwm1.duty_ns(2200000)
    eyesToggle()
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
        utime.sleep(0.5)
        mg2.toggle()
        mg3.toggle()
        utime.sleep(0.5)
        mg3.toggle()
        er2.toggle()
        utime.sleep(0.5)
        er2.toggle()
        er1.toggle()
        utime.sleep(0.5)
        er1.toggle()
        mg1.toggle()
        utime.sleep(0.5)
        mg1.toggle()
        mg2.toggle()
        utime.sleep(0.5)
        mg2.toggle()
        mg3.toggle()
        utime.sleep(0.5)
        mg3.toggle()
        er2.toggle()
        utime.sleep(0.5)
        er2.toggle()
        er1.toggle()
        utime.sleep(0.5)
        er1.toggle()
        mg1.toggle()
        utime.sleep(0.5)
        mg1.toggle()
        mg2.toggle()
        utime.sleep(0.5)
        mg2.toggle()
    print("runningFace ran.")
    print("Temp *C: ", temp)
    print("Current VDC: ", voltage)
    print("lightPowerValue: ", lightPowerValue)
    
def goCrazy():
    for i in range(20):
        anyLED = random.choice(leds)
        anyLED.toggle()
        utime.sleep(0.2)
        anyLED.toggle()

def lightsOnlyMode():
    for i in range(9):
        randomFunction = random.choice(lightsOnly)
        randomFunction()
        utime.sleep(1)
    print("lightsOnly cycle complete, shell open...")    

# ------------------- compound functions -------------
def standAndDeliver():
    leds.value(0)
    utime.sleep(0.5)

def startUp():
    print(".*.*.*")
    utime.sleep(1)
    print("starting up ...")			#text based UX/UI concept?    
    print(".*.*.*")
    utime.sleep(1)
    goCrazy()
    print(".*.*.*")
    utime.sleep(1)    
    runningFace()
    print(".*.*.*")
    utime.sleep(1)    
    if lightPowerValue < 2.4:					#if statement referencing photocell resistor 
        print(".*.*.*")
        utime.sleep(1)
        print("data suggests low light conditions")
        sam.say("fuck its dark here")
        print(".*.*.*")
        utime.sleep(1)
        activateLightsOnly = input("activate lights only? : ") #single line will set the object and print the input req 
        utime.sleep(0.5)
        if activateLightsOnly == "yes": #if statement dependent on input
            lightsOnlyMode()
            #for i in range(9):
                #randomFunction = random.choice(lightsOnly)
                #randomFunction()
                #utime.sleep(1)
            #print("lightsOnly cycle complete, shell open...")
        else:
            print("moot")
            
            
        
    else:
        print("suns out guns out !")
        utime.sleep(1)
        selectMode = input("please select mode...")
        utime.sleep(0.5)
        if selectMode == "lightsOnly":
            lightsOnly()
        else:
            print("Error - rtn home")
            

    
  
# Put the function names directly in the list (no parentheses)
functions = [runningFace, eyes_sequence, mouth_sequence, zombieMode, arm_ss_a, arm_ss_b, arm_ss_c, eye_blink, mouth_led_sequence, hybernate, buzzerTest]
lightsOnly = [runningFace, eyes_sequence, mouth_sequence, eye_blink, mouth_led_sequence, hybernate, buzzerTest]





#---------------------random choice of function sequences from array of functions-------------
#while True:
    #runRandom = random.choice(lightsOnly)
    
    # Run the function that was picked
    #runRandom()
    
    # Pause so it doesn't run at light speed
    #utime.sleep(1)
    #print(voltage)
    

# ---- testing elrs radio ----
#radio master rp3 on pico

while True:
    radioData = ElrsRx.read()
    print("radioData: ", radioData)
    utime.sleep(3)
    newRadioData = ElrsRx.read()
    if newRadioData != radioData:
        eyes_sequence()
        utime.sleep(3)
    else:
        print("same")

       