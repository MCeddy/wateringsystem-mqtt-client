import MySQLdb
import _mysql_exceptions


class DataService:
    def __init__(self, mysql_config):
        self.config = mysql_config
        try:
            self.db = MySQLdb.connect(host=mysql_config['host'],
                                      db=mysql_config['database'],
                                      user=mysql_config['user'],
                                      passwd=mysql_config['password'])
        except _mysql_exceptions.OperationalError:
            print('couldn\'t connect to MySQL database')

    def save_temperature(self, value):
        pass
