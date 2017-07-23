import MySQLdb


class DataService:
    def __init__(self, mysql_config):
        self.config = mysql_config
        #self.__connect()

    def __connect(self):
        self.db = MySQLdb.connect(host=self.config['host'],
                                  db=self.config['database'],
                                  user=self.config['user'],
                                  passwd=self.config['password'])

    def save_sensor_values(self, temperature, humidity, soil_moisture):
        pass
