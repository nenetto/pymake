from datalab_utils.sql.database import DataBase
import psycopg2

class Zitycar(DataBase):

    def __init__(self):
        super().__init__()
        # DB connection info
        self._host = '54.194.159.222'
        self._port = 5006
        self._dbname = 'cars'
        self._user = 'ds_privileges'
        self._pwd = 'jN7gJ23LHcdnMjHJ'

    def connect(self):

        if not self._connected:
            connection_string = "host='{}' port={} dbname='{}' user={} password={}".format(self._host,
                                                                                           self._port,
                                                                                           self._dbname,
                                                                                           self._user,
                                                                                           self._pwd)
            try:
                self._connection = psycopg2.connect(connection_string)
            except Exception as e:
                print('[Zitycar]: Error connecting to database')
                print('-'*50)
                print(e)
                print('-')
                self._connected = False

            self._connected = True

    def disconnect(self):
        if self._connected:
            self._connection.close()
            self._connected = False
