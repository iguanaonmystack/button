# Trinket IO demo
# Welcome to CircuitPython 3.1.1 :)

import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogOut, AnalogIn
import touchio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import adafruit_dotstar as dotstar
import time
import usb_cdc

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Analog input on D0
#analog1in = AnalogIn(board.D0)

# Analog output on D1
#aout = AnalogOut(board.D1)

# Digital input with pullup on D2
red = DigitalInOut(board.D2)
red.direction = Direction.OUTPUT
red.value = False
# button.pull = Pull.UP  # inputs only

# BUTTON
button = DigitalInOut(board.D0)
button.direction = Direction.INPUT
button.pull = Pull.UP

# Capacitive touch on D3
#touch = touchio.TouchIn(board.D3)

# Used if we do HID output, see below
kbd = Keyboard(usb_hid.devices)

# For serial communications
serial = usb_cdc.data

######################### HELPERS ##############################

# Helper to convert analog input to voltage
def getVoltage(pin):
    return (pin.value * 3.3) / 65536

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return (0, 0, 0)
    if (pos > 255):
        return (0, 0, 0)
    if (pos < 85):
        return (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))

######################### MAIN LOOP ##############################

i = 0
pressed = False
flashing = 0
while True:
    # spin internal LED around! autoshow is on
    #dot[0] = wheel(i & 255)
    dot[0] = (128, 128, 128) if pressed else (128, 0, 0)

    # set analog output to 0-3.3V (0-65535 in increments)
    #aout.value = i * 256

    # Read analog voltage on D0
    #print("D0: %0.2f" % getVoltage(analog1in))

    # Cycle the LED hooked up to D2
    if flashing > 0:
        print('flashing led', flashing, i, (i // 16), (i // 16) % 2)
        if (i // 16) % 2:
            red.value = False
        else:
            red.value = True
            flashing -= 1
    else:
        red.value = False

    # use D3 as capacitive touch to turn on internal LED
    #if touch.value:
    #    print("D3 touched!")
    #led.value = touch.value

    if not button.value:
        #print("Button on D0 pressed!")
        if not pressed:
            print("button keydown")
            serial.write(b'PRESS\n')
            pressed = True
    else:
        #print("Button on D0 not pressed!")
        # optional! uncomment below & save to have it sent a keypress
        #kbd.press(Keycode.A)
        #kbd.release_all()
        if pressed:
            print("button keyup")
            pressed = False

    # Check for incoming data
    while serial.in_waiting > 0:
        instruction = serial.readline()
        print(instruction)
        if instruction == b"BUTTON?\n":
            # A very rudimentary handshake
            serial.write(b'BUTTON!\n')
        elif instruction == b"FLASH\n":
            # Flash the LED a bit
            flashing = 50

    i = (i+1) % 256  # run from 0 to 255
    time.sleep(0.01) # make bigger to slow down

