import time
import math
import cPickle as pickle
import paho.mqtt.publish as publish
from roboclaw import Roboclaw

MQTT_SERVER1 = "143.215.103.106" #sub to which message should be sent
MQTT_SERVER2 = "143.215.106.181"
MQTT_PATH_T = "T_channel"
MQTT_PATH_S = "S_channel"

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

    return [tics_move1, speed_move1, tics_move2, speed_move2]


def dist_time(x, y, time):  #function to have start and finish at same time
    speed_move1 = 0
    speed_move2 = 0

    dist_move1 = triangulate(x1, y1) - triangulate(x1 - x, y1 - y) #using trig to find length of Z
    dist_move2 = triangulate(x2, y2) - triangulate(x2 + x, y2 - y)

    tics_move1 = distance_to_pulse(math.fabs(dist_move1))
    tics_move2 = distance_to_pulse(math.fabs(dist_move2))

    if(dist_move1 > 0):    #negative distance wont make it move backwards, negative speed will
        speed_move1 = -int(tics_move1 / time)
    else:
        speed_move1 = int(tics_move1 / time)

    if(dist_move2 > 0):
        speed_move2 = -int(tics_move2 / time)
    else:
        speed_move2 = int(tics_move2 / time)

    return [tics_move1, speed_move1, tics_move2, speed_move2]

def mqtt_server_time(x_in, y_in, time_in):
    data = dist_time(x_in, y_in, time_in)

    publish.single(MQTT_PATH_T, data[0], hostname = MQTT_SERVER1)
    publish.single(MQTT_PATH_S, data[1], hostname = MQTT_SERVER1)

    publish.single(MQTT_PATH_T, data[2], hostname = MQTT_SERVER2)
    publish.single(MQTT_PATH_S, data[3], hostname = MQTT_SERVER2)


def mqtt_server_dist(x, y):
    dist_time(x_in, y_in)

    publish.single(MQTT_PATH_T, data[0], hostname = MQTT_SERVER1)
    publish.single(MQTT_PATH_S, data[1], hostname = MQTT_SERVER1)

    publish.single(MQTT_PATH_T, data[2], hostname = MQTT_SERVER2)
    publish.single(MQTT_PATH_S, data[3], hostname = MQTT_SERVER2)

def write_origin():
    pickle.dump([str(21.5), str(52.0)], open('data_pickle.pickle', 'wb'))
    return "Location centered at zero"

def read_current():
    test = pickle.load(open('data_pickle.pickle', 'rd'))
    return test

