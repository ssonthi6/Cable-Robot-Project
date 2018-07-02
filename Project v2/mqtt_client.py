import paho.mqtt.client as mqtt
import math
from roboclaw import Roboclaw
import cPickle as pickle

MQTT_SERVER = "localhost"
MQTT_PATH_S = "S_channel"
MQTT_PATH_T = "T_channel"

rc = Roboclaw("/dev/ttyACM0",115200) #RPI port 1 USB
rc.Open()
address = 0x80

input_values = []

enc_values = []

def on_connect(client, userdata, flags, rc):
        print("connected with result code " + str(rc))
        client.subscribe(MQTT_PATH_S)
        client.subscribe(MQTT_PATH_T)

def on_message(client, userdata, msg):
        raw_data = str(msg.payload)
        print(msg.topic + " " + str(msg.payload))
        input_values.append(raw_data)
        print(input_values)
        
        if(len(input_values) == 2):
                bool_init = True
                while(bool_init):
                        rc.SpeedM1(address, int(input_values[1]))
                        enc = rc.ReadEncM1(address)
                        enc_values.append(enc[1])
                        total_distance_gone = math.fabs(enc_values[-1]
                                                        - enc_values[0])
                        correction_dist = int(int(input_values[0])
                                              - total_distance_gone)

                        if(total_distance_gone >= int(input_values[0])):
                                rc.SpeedM1(address, 0)
                                enc_values[:] = []
                                bool_init = False

                print("tics off: " + str(correction_dist))
                input_values[:] = []
                
        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()

