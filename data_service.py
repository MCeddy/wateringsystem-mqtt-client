import MySQLdb, _mysql_exceptions
import logging


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
        pass

    def __del__(self):
        try:
            self.__db.close()
        except:
            pass
