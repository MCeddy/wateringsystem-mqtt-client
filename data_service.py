import MySQLdb


class DataService:
    def __init__(self, mysql_config):
        self.config = mysql_config
        self.db = MySQLdb.connect(host=mysql_config['host'],
                                  db=mysql_config['database'],
                                  user=mysql_config['user'],
                                  passwd=mysql_config['password'])

    def save_temperature(self, value):
        pass
