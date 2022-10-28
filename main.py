#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch

import struct

# Declare motors 
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
arm_motor = Motor(Port.A)
forward = 0
left = 0
right = 0


# Auto center steering wheels.
arm_motor.run_until_stalled(250)
arm_motor.reset_angle(80)
arm_motor.run_target(300,0)


# A helper function for converting stick values (0 - 255)
# to more usable numbers (-100 - 100)
def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
 
    val: float or int
    src: tuple
    dst: tuple
 
    example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
    """
    return (float(val-src[0]) / (src[1]-src[0])) * (dst[1]-dst[0])+dst[0]


# Open the Gamepad event file:
# /dev/input/event3 is for PS3 gamepad
# /dev/input/event4 is for PS4 gamepad
# look at contents of /proc/bus/input/devices if either one of them doesn't work.
# use 'cat /proc/bus/input/devices' and look for the event file.
infile_path = "/dev/input/event4"

# open file in binary mode
in_file = open(infile_path, "rb")

# Read from the file
# long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'    
EVENT_SIZE = struct.calcsize(FORMAT)
event = in_file.read(EVENT_SIZE)

while event:
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)
#left and right bumper control arm_motor code
# IN PROGRESS IT PROBABLY WON'T WORK




    if ev_type == 1:
        if code == 310 and value == 1:
            right = 80
            print(arm_motor.angle())
        if code == 310 and code == 311 and value == 0:
            right = 0
            print(arm_motor.angle())
        if code == 311 and value == 1:
            right = -80
            print(arm_motor.angle())
        if code == 310 and code == 311 and value == 1:
            right = 0
        
    
    #right stick code
    elif ev_type == 3: # Stick was moved
        if code == 0: 
            left = scale(value, (0,255), (40, -40))
        if code == 5:
            forward = scale(value, (0,255), (0,-100))
        if code == 2:
            forward = scale(value, (0,255), (0,100))

        


        
    # Set motor voltages. 
    left_motor.dc(forward - left)
    right_motor.dc(forward + left)

    # Track the steering angle
    arm_motor.track_target(right)

    # Finally, read another event
    event = in_file.read(EVENT_SIZE)

in_file.close()
