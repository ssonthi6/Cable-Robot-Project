import time
import math
from roboclaw import Roboclaw

rc1 = Roboclaw("/dev/ttyACM0",115200)
rc2 = Roboclaw("/dev/ttyACM1",115200)

inch_per_pulse = 0.0007559933
speed = 2400
width = 43.0 #inches
height = 52.0 #inches

#variables to store - x1, y1/y2
x1 = width / 2
x2 = width - x1
y1 = y2 = height #need to change use of height

def distance_to_pulse(distance):
    return int(distance/inch_per_pulse)

def triangulate(x, y):
    return math.sqrt(math.pow(x,2) + math.pow(y,2))

def dist_vertical(y_input):
    #dist_move = math.fabs(triangulate(width, height)
    #                     - triangulate(width, height - y))
    #speed_actual = 0
    #tics_move = distance_to_pulse(dist_move)
    
    #if(y > 0):
    #    speed_actual = -speed
    #else:
    #    speed_actual = speed

    #rc1.SpeedDistanceM1(address, speed_actual, tics_move, 0)
    #rc2.SpeedDistanceM1(address, speed_actual, tics_move, 0)

    dist_2D(0, y_input)

def dist_horizontal(x_input):
    dist_2D(x_input, 0)

def dist_2D(x, y):
    speed_move1 = 0
    speed_move2 = 0

    dist_move1 = triangulate(x1, y1) - triangulate(x1 - x, y1 - y)
    dist_move2 = triangulate(x2, y2) - triangulate(x2 + x, y2 - y)

    tics_move1 = distance_to_pulse(math.fabs(dist_move1))
    tics_move2 = distance_to_pulse(math.fabs(dist_move2))

    if(dist_move1 > 0):
        speed_move1 = -speed
    else:
        speed_move1 = speed

    if(dist_move2 > 0):
        speed_move2 = -speed
    else:
        speed_move2 = speed

    rc1.SpeedDistanceM1(address, speed_move1, tics_move1, 0)
    rc2.SpeedDistanceM1(address, speed_move2, tics_move2, 0)

rc1.Open()
rc2.Open()
address = 0x80

#dist_vertical(-10)
#dist_2D(-10, 0)
        

rc1.SpeedDistanceM1(address,1800, 1200 ,0)
