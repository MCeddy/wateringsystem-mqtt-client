import paho.mqtt.client as mqtt
import argparse
import json

from data_service import DataService
from config_service import ConfigService


def load_args():
    # setup commandline argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--env')

    return parser.parse_args()


def create_mqtt_client(config):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(config['user'], config['password'])
    client.connect(config['host'], config['port'])

    return client


def on_connect(client, userdata, flags_dict, rc):
    if rc != 0:
        print('MQTT connection error: ' + str(rc))
        return

    print('MQTT connected')

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_config['topic'])


def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))

    sensor_values = json.loads(msg.payload.decode('utf-8'))

    temperature = sensor_values['Temperature']
    humidity = sensor_values['Humidity']
    soil_moisture = sensor_values['SoilMoisture']

    data_service.save_sensor_values(temperature, humidity, soil_moisture)

args = load_args()

config_service = ConfigService(args.env)
mqtt_config = config_service.get_section('mqtt')
mysql_config = config_service.get_section('mysql')

data_service = DataService(mysql_config)

mqtt_client = create_mqtt_client(mqtt_config)
mqtt_client.loop_forever()
