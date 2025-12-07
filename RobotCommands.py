import ConvexHullTakeTwo as Conv
import PolygonBreakdown as Poly
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, MoveTank
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor import IN1
import math

img = Conv.getImage()
img_contours, img_hier = Conv.prepImage(img)
hulls = Conv.makeConvexHulls(img_contours, img_hier, img)

shortestCoords = Poly.getShortestPathCoords(hulls, img)

robot = MoveTank(OUTPUT_B, OUTPUT_C)
gyro = GyroSensor(IN1) # sets up gyro: sensor that records angle rotated
gyro.reset()

driveSpeed = 50
turnSpeed = 15

"""
Make following functions:
- Turns robot
- Drives robot
- Normalizes angles
"""

classroomWidth = 607
classroomLength = 396
classroomWidthInFeet = 35.166666666
classroomLengthInFeet = 23.25
scalingFactor = ((classroomWidthInFeet/classroomWidth) + (classroomLengthInFeet/classroomLength))/2

def computeDistance(currCoord, nextCoord):
    distx = nextCoord[0] - currCoord[0]
    disty = nextCoord[1] - currCoord[1]
    dist = math.sqrt(distx**2 + disty**2) * scalingFactor
    return dist


