#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

# Initialize EV3 and motors
ev3 = EV3Brick()
left = Motor(Port.B)
right = Motor(Port.C)

ev3.speaker.say("Motor test starting")

# Rotate both motors forward
left.run_angle(300, 360)   # speed deg/s, angle deg
right.run_angle(300, 360)

wait(500)

# Rotate both motors backward
left.run_angle(300, -360)
right.run_angle(300, -360)

ev3.speaker.say("Test complete")
