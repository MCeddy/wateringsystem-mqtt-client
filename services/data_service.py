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
            self.__conn = MySQLdb.connect(host=self.__config['host'],
                                          db=self.__config['database'],
                                          user=self.__config['user'],
                                          passwd=self.__config['password'])
            self.__log.info('MySQL connected')
        except _mysql_exceptions.OperationalError:
            self.__log.error('couldn\'t connect to MySQL database', exc_info=True)

    def __execute(self, sql):
        try:
            cursor = self.__conn.cursor()
            result = cursor.execute(sql)
            return result, cursor
        except (AttributeError, MySQLdb.OperationalError):
            self.__connect()  # reconnect

            cursor = self.__conn.cursor
            result = cursor.execute(sql)
            return result, cursor

    def save_sensor_values(self, temperature, humidity, soil_moisture):
        try:
            sql_command = 'INSERT INTO sensors (temperature, humidity, soil_moisture) VALUES ({}, {}, {})' \
                .format(temperature, humidity, soil_moisture)
            result, cursor = self.__execute(sql_command)
            self.__conn.commit()

            if result == 1:
                self.__log.debug('saving sensor-values: successful')
                return cursor.lastrowid
            else:
                self.__log.error('saving sensor-values: error')
        except _mysql_exceptions.DatabaseError:
            self.__log.error('error on saving data', exc_info=True)
            self.__conn.rollback()

    def save_watering(self, watering_milliseconds):
        try:
            sql_command = 'INSERT INTO watering (milliseconds) VALUES ({})' \
                .format(watering_milliseconds)
            result, cursor = self.__execute(sql_command)
            self.__conn.commit()

            if result == 1:
                self.__log.debug('saving watering: successful')
                return cursor.lastrowid
            else:
                self.__log.error('saving watering: error')

        except _mysql_exceptions.DatabaseError:
            self.__log.error('error on saving data', exc_info=True)
            self.__conn.rollback()

    def __del__(self):
        if self.__conn.open == 1:
            self.__conn.close()
