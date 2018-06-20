import paho.mqtt.client as mqtt
import cPickle as pickle
import kinematics as k

MQTT_SERVER = "localhost"
MQTT_PATH_S = "S_channel"
MQTT_PATH_T = "T_channel"

input_values = []

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
                input_values[:] = []
                
        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()

