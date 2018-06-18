import paho.mqtt.publish as publish

MQTT_SERVER = "143.215.103.106"
MQTT_PATH = "test_channel"

publish.single(MQTT_PATH, "Hello World!", hostname = MQTT_SERVER)
