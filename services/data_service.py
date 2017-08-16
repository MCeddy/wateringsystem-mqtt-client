import logging

import MySQLdb
import _mysql_exceptions


class DataService:
    def __init__(self, mysql_config):
        self.__log = logging.getLogger(__name__)
        self.__config = mysql_config
        self.__connect()

    def __connect(self):
        try:
            self.__db = MySQLdb.connect(host=self.__config['host'],
                                        db=self.__config['database'],
                                        user=self.__config['user'],
                                        passwd=self.__config['password'])
            self.__log.info('MySQL connected')
        except _mysql_exceptions.OperationalError:
            self.__log.error('couldn\'t connect to MySQL database', exc_info=True)

    def save_sensor_values(self, temperature, humidity, soil_moisture):
        try:
            cursor = self.__db.cursor()

            sql_command = 'INSERT INTO sensors (temperature, humidity, soil_moisture) VALUES ({}, {}, {})' \
                .format(temperature, humidity, soil_moisture)
            result = cursor.execute(sql_command)
            self.__db.commit()

            if result == 1:
                self.__log.debug('saving sensor-values: successful')
                return cursor.lastrowid
            else:
                self.__log.error('saving sensor-values: error')
        except _mysql_exceptions.DatabaseError:
            self.__log.error('error on saving data', exc_info=True)
            self.__db.rollback()

    def save_watering(self, watering_milliseconds):
        try:
            cursor = self.__db.cursor()

            sql_command = 'INSERT INTO watering (milliseconds) VALUES ({})' \
                .format(watering_milliseconds)
            result = cursor.execute(sql_command)
            self.__db.commit()

            if result == 1:
                self.__log.debug('saving watering: successful')
                return cursor.lastrowid
            else:
                self.__log.error('saving watering: error')

        except _mysql_exceptions.DatabaseError:
            self.__log.error('error on saving data', exc_info=True)
            self.__db.rollback()

    def __del__(self):
        if self.__db.open == 1:
            self.__db.close()
