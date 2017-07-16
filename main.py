import paho.mqtt.client as mqtt
import argparse

from data_service import DataService
from config_service import ConfigService


def on_connect(client, userdata, flags_dict, rc):
    if rc != 0:
        print('connection error: ' + str(rc))
        return

    print('connected')

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_config['topic'])


def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))

    if msg.topic == 'wateringsystem/sensors/dht11/temperature':
        data_service.save_temperature(msg.payload)
    elif msg.topic == 'wateringsystem/sensors/dht11/humidity':
        pass
    elif msg.topic == 'wateringsystem/sensors/soil-moisture':
        pass

# setup commandline argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--env')
args = parser.parse_args()

config_service = ConfigService(args.env)
mqtt_config = config_service.get_section('mqtt')
mysql_config = config_service.get_section('mysql')
data_service = DataService(mysql_config)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(mqtt_config['user'], mqtt_config['password'])

client.connect(mqtt_config['host'], mqtt_config['port'])

client.loop_forever()
