import MySQLdb
import _mysql_exceptions


class DataService:
    def __init__(self, mysql_config):
        self.config = mysql_config
        self.__connect()

    def __connect(self):
        try:
            self.db = MySQLdb.connect(host=self.config['host'],
                                      db=self.config['database'],
                                      user=self.config['user'],
                                      passwd=self.config['password'])
        except _mysql_exceptions.OperationalError:
            print('couldn\'t connect to MySQL database')

    def save_sensor_values(self, temperature, humidity, soil_moisture):
        pass
