"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 10-05-2018
"""

from pymake.utils.sql.database import DataBase


class MsSQL(DataBase):

    def __init__(self, host, port, dbname, user, pwd, verbose=True):
        super().__init__(host, port, dbname, user, pwd, verbose)

    def connect(self):

        if not self._connected:
            connection_string = 'DRIVER={ODBC Driver 13 for SQL Server};'
            connection_string += 'SERVER={0};DATABASE={1};UID={2};PWD={3};'.format(self._host,
                                                                                   self._dbname,
                                                                                   self._user,
                                                                                   self._pwd)
            try:
                import pyodbc
            except ImportError:
                self.pm.print_error('Package pyodbc is not installed')
                self.pm.print_error('You have installation recipes in package pydockerutils @')
                self.pm.print_error('  - [https://github.com/nenetto/pydockerutils]')
                self.pm.print_error('Exiting', exit_code=1)


            try:
                self._connection = pyodbc.connect(connection_string)
            except Exception as e:
                self.pm.print_error('Error connecting to database')
                self.pm.print_error(str(e))
                self.pm.print_separator()
                self._connected = False
                return

            self._connected = True

            if self._verbose:
                self.pm.print_info('Connection Success')

    def disconnect(self):
        if self._connected:
            self._connection.close()
            self._connected = False
            if self._verbose:
                self.pm.print_info('Disconnection Success')