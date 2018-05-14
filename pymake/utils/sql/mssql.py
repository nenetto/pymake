"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 10-05-2018
"""

from pymake.utils.sql.database import DataBase
from pymake.main import printer as pm

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
                pm.print_error('Package pyodbc is not installed')
                try:
                    import pydockerutils
                except ImportError:
                    pm.print_error('You have installation recipes in package pydockerutils @')
                    pm.print_error('  - [https://github.com/nenetto/pydockerutils]')
                    pm.print_error('Exiting', exit_code=1)

                pm.print_warning('Please, run the command install_pyodb from pydockerutils in the shell')


            try:
                self._connection = pyodbc.connect(connection_string)
            except Exception as e:
                pm.print_error('Error connecting to database')
                pm.print_error(str(e))
                pm.print_separator()
                self._connected = False
                return

            self._connected = True

            if self._verbose:
                pm.print_info('Connection Success')

    def disconnect(self):
        if self._connected:
            self._connection.close()
            self._connected = False
            if self._verbose:
                pm.print_info('Disconnection Success')