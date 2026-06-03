# By: m3ch-l0rd
# Date: 06022026
# most successful micropython crsf protocol 
# maps "servo0" & "servo1" to "pitch" and "roll" on the right joystick of my radiomaster zorro transmitter 
import time
from machine import UART, Pin, PWM

# 1. Configure UART
# Use the correct UART pins for your specific microcontroller
# Example for ESP32: TX=17, RX=16
uart = UART(1, baudrate=420000, tx=Pin(4), rx=Pin(5), bits=8, parity=None, stop=1)

def parse_crsf_channels():
    if uart.any() < 24: # CRSF RC Channel packet is typically 24 bytes long
        return None
        
    data = uart.read(24)
    
    # 2. Frame Validation
    # CRSF structure: [Header(0xC8)] [Length(24)] [Type(0x16)] [16 Channels] [CRC]
    if data[0] != 0xC8 or data[2] != 0x16:
        return None
        
    # 3. 11-bit Channel Unpacking
    # Extract raw 11-bit values (range 172 to 1811)
    # The bit-math maps to standard CRServoF/ExpressLRS telemetry specifications
    ch = [0] * 16
    ch[0]  = ((data[3] | (data[4] << 8)) & 0x07FF)
    ch[1]  = ((data[4] >> 3 | (data[5] << 5)) & 0x07FF)
    ch[2]  = ((data[5] >> 6 | (data[6] << 2) | (data[7] << 10)) & 0x07FF)
    ch[3]  = ((data[7] >> 1 | (data[8] << 7)) & 0x07FF)
    ch[4]  = ((data[8] >> 4 | (data[9] << 4)) & 0x07FF)
    ch[5]  = ((data[9] >> 7 | (data[10] << 1) | (data[11] << 9)) & 0x07FF)
    
    return ch

OFF = 0000000
MIN = 500000
LOW = 1000000
MID = 1500000
HIG = 2000000
MAX = 2500000

servo0 = PWM(Pin(0)) # left arm 
servo0.freq(50)
servo0.duty_ns(MID)

servo1 = PWM(Pin(20)) # right arm 
servo1.freq(50)
servo1.duty_ns(MID)

# 4. Main Execution Loop
while True:
    channels = parse_crsf_channels()
    
    if channels is not None:
        # Map values to specific variables (Typically Throttle, Yaw, Pitch, Roll)
        # CRSF range is mapped 172 (min), 992 (center), 1811 (max)
        yaw = channels[3]
        pitch = channels[1]  #swapped yaw and roll 
        throttle = channels[2]
        roll = channels[0]
        
        # Display variables
        print(f"Yaw: {yaw} | Pitch: {pitch} | Throttle: {throttle} | Roll: {roll}")
        
    # change indentation to try and make multi channels work to servo.... doesnt work yaw pitch throttle roll are not global
        if pitch > 1600:
            servo0.duty_ns(MAX)
            servo1.duty_ns(MIN)
        elif pitch < 400:
            servo0.duty_ns(MIN)
            servo1.duty_ns(MAX)
        #else:
            #servo0.duty_ns(MID)
            #servo1.duty_ns(MID)
            
            #time.sleep(0.01)    #response from roll and pitch at the same time but it tries to return to MID constantly (makes sense...)    
            
        elif roll > 1600:
            servo0.duty_ns(MAX)
            servo1.duty_ns(MAX)
        elif roll < 800:
            servo0.duty_ns(MIN)
            servo1.duty_ns(MIN)
        else:
            servo0.duty_ns(MID)
            servo1.duty_ns(MID)            
        
            time.sleep(0.01) # Poll at 100Hz
    
