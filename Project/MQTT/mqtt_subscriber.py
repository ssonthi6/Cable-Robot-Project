import paho.mqtt.client as mqtt

MQTT_SERVER = "localhost"
MQTT_PATH = "test_channel"

def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))
	client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
