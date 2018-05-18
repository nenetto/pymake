"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 10-05-2018
"""

import psycopg2
from pymake.utils.sql.database import DataBase
from pymake.main import printer as pm


class Postgres(DataBase):

    def __init__(self, host, port, dbname, user, pwd):
        super().__init__(host, port, dbname, user, pwd)

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
                pm.print_error('Error connecting to database')
                pm.print_separator()
                pm.print_error(str(e))
                pm.print_separator()
                self._connected = False

            self._connected = True

    def disconnect(self):
        if self._connected:
            self._connection.close()
            self._connected = False
