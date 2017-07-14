import paho.mqtt.client as mqtt

MQTT_BROKER = 'mqtt.my-broker.org'
MQTT_PORT = 1883
MQTT_USER = ''
MQTT_PASSWORD = ''
MQTT_TOPIC = 'wateringsystem/#'


def on_connect(client, userdata, flags_dict, rc):
    print('connected with result code ' + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.connect(MQTT_BROKER, MQTT_PORT)

client.loop_forever()
