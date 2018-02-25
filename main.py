import argparse
import json
import logging
import logging.config
import os

import paho.mqtt.client as mqtt
import yaml

from services.data_service import DataService
from services.watering_service import WateringService
from services.config_service import ConfigService


def load_args():
    # setup commandline argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--env')

    return parser.parse_args()


def setup_logging(default_level=logging.INFO):
    path = os.path.join(os.getcwd(), 'config', 'logging.yml')

    if os.path.exists(path):
        # load from config
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def create_mqtt_client(config):
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    user = config['user']
    if user is not None:
        # use authentication
        client.username_pw_set(user, config['password'])

    client.connect(config['host'], config['port'])

    return client


def handle_receive_sensor_values(payload):
    if payload is None:
        return

    try:
        # transform payload to JSON
        sensor_values = json.loads(payload.decode('utf-8'))

        temperature = int(sensor_values['Temperature'])
        humidity = int(sensor_values['Humidity'])
        soil_moisture = int(sensor_values['SoilMoisture'])

        sensors_id = data_service.save_sensor_values(temperature, humidity, soil_moisture)

        if sensors_id is None:
            return

        watering_milliseconds = watering_service.calculate_milliseconds(soil_moisture)

        if watering_milliseconds > 200:
            watering(watering_milliseconds)
    except AttributeError:
        logger.error('read sensors JSON error', exc_info=True)
    except ValueError:
        logger.error('convert sensor-values error', exc_info=True)


def handle_watering(payload):
    try:
        watering_milliseconds = int(payload)
        data_service.save_watering(watering_milliseconds)
    except ValueError:
        logger.error('convert watering-milliseconds error', exc_info=True)


def watering(milliseconds):
    mqtt_client.publish(mqtt_config['topics']['watering'], milliseconds)


def on_connect(client, userdata, flags_dict, rc):
    if rc != 0:
        logger.error('MQTT connection error: ' + str(rc))
        return

    logger.info('MQTT connected')

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_config['topics']['generic'])


def on_message(client, userdata, msg):
    logger.debug('receive message "%s": %s', msg.topic, str(msg.payload))

    if msg.topic == mqtt_config['topics']['sensors']:  # sensor values
        handle_receive_sensor_values(msg.payload)
    if msg.topic == mqtt_config['topics']['watering']:  # watering
        handle_watering(msg.payload)


args = load_args()
setup_logging()
logger = logging.getLogger(__name__)

logger.info('starting MQTT client')

try:
    config_service = ConfigService(args.env)
    mqtt_config = config_service.get_section('mqtt')
    mysql_config = config_service.get_section('mysql')
    watering_config = config_service.get_section('watering')

    data_service = DataService(mysql_config)
    watering_service = WateringService(watering_config)

    mqtt_client = create_mqtt_client(mqtt_config)
    mqtt_client.loop_forever()
except Exception as error:
    logger.error('main error', exc_info=True)
