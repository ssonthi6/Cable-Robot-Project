import time
import math
import cPickle as pickle
from roboclaw import Roboclaw

rc1 = Roboclaw("/dev/ttyACM0",115200) #currently only working on 1 rpi
rc2 = Roboclaw("/dev/ttyACM1",115200)

inch_per_pulse = 0.0007559933 #experimental value - yet to be tested well
speed = 2400
width = 43.0 #inches
height = 52.0 #inches

#variables to store - x1, y1
x1 = float(pickle.load(open('data_pickle.pickle', 'rd'))[0])
x2 = width - x1
y1 = y2 = float(pickle.load(open('data_pickle.pickle', 'rd'))[1])
def distance_to_pulse(distance):
    return int(distance/inch_per_pulse) #roboclaw can only take an int

def triangulate(x, y):
    return math.sqrt(math.pow(x,2) + math.pow(y,2))

def DistanceTime(distance, time):
    speed = distance / time

def dist_vertical(y_input):
    dist_2D(0, y_input)

def dist_horizontal(x_input):
    dist_2D(x_input, 0)

def dist_2D(x, y):
    speed_move1 = 0
    speed_move2 = 0

    dist_move1 = triangulate(x1, y1) - triangulate(x1 - x, y1 - y) #using trig to find length of Z
    dist_move2 = triangulate(x2, y2) - triangulate(x2 + x, y2 - y)

    tics_move1 = distance_to_pulse(math.fabs(dist_move1))
    tics_move2 = distance_to_pulse(math.fabs(dist_move2))

    if(dist_move1 > 0):    #negative distance wont make it move backwards, negative speed will
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
