import paho.mqtt.client as mqtt
import cPickle as pickle
import kinematics as k

MQTT_SERVER = "localhost"
MQTT_PATH_X = "X_channel"
MQTT_PATH_Y = "Y_channel"
MQTT_PATH_T = "T_channel"

input_values = []

def on_connect(client, userdata, flags, rc):
        print("connected with result code " + str(rc))
        client.subscribe(MQTT_PATH_X)
        client.subscribe(MQTT_PATH_Y)
        client.subscribe(MQTT_PATH_T)

def on_message(client, userdata, msg):
        raw_data = str(msg.payload)
        print(msg.topic + " " + str(msg.payload))
        input_values.append(raw_data)
        print(input_values)
        
        if(len(input_values) == 3):
                origin = [21.5, 52.0]
                try:
                        pos = pickle.load(open('data_pickle.pickle', 'rd'))
                except (OSError, IOError) as e:
                        pos = origin
                        pickle.dump(pos, open('data_pickle.pickle', 'wb'))
                k.dist_time(float(input_values[0]),
                            float(input_values[1]),
                            float(input_values[2]))
                x1 = float(pos[0]) + float(input_values[0])
                y1 = float(pos[1]) - float(input_values[1])
                updated_data = [x1, y1]
                pickle.dump(updated_data, open('data_pickle.pickle', 'wb'))
                input_values[:] = []
                
        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()

