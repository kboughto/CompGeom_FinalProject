#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C
from time import sleep

left = LargeMotor(OUTPUT_B)
right = LargeMotor(OUTPUT_C)

print("Motor test starting")

# forward 1 rotation
left.on_for_rotations(20, 1)
right.on_for_rotations(20, 1)

sleep(0.5)

# backward 1 rotation
left.on_for_rotations(20, -1)
right.on_for_rotations(20, -1)

print("Motor test complete")
