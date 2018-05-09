import psycopg2
from pymake.utils.sql.database import DataBase
from pymake.utils.common.common_functions import read_env_var


class Zitycar(DataBase):

    def __init__(self):
        super().__init__()

        # DB connection info
        self._host = read_env_var('ZITYCAR_HOST')
        self._port = read_env_var('ZITYCAR_PORT')
        self._dbname = read_env_var('ZITYCAR_DBNAME')
        self._user = read_env_var('ZITYCAR_USER')
        self._pwd = read_env_var('ZITYCAR_PWD')

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
                self.pm.print_error('Error connecting to database')
                self.pm.print_separator()
                self.pm.print_error(str(e))
                self.pm.print_separator()
                self._connected = False

            self._connected = True

    def disconnect(self):
        if self._connected:
            self._connection.close()
            self._connected = False
