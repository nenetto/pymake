"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 10-05-2018
"""

import pyodbc
from pymake.utils.sql.database import DataBase
from pymake.utils.common.prettymessaging import PrettyMessaging
from pymake.utils.common.scripting import run_commands
import pkg_resources
import sys


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
                self._connection = pyodbc.connect(connection_string)
            except Exception as e:
                self.pm.print_error('Error connecting to database')
                self.pm.print_error('Did you install MSSQL drivers?')
                MsSQL.install()
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

    @staticmethod
    def install():

        pm = PrettyMessaging('Pymake DataBase MSSQL')

        # Check platform
        if sys.platform.startswith('linux'):
            pm.print_info('Installing MSSQL Drivers')

            script = pkg_resources.resource_filename('pymake', 'utils/sql/MSSQL_drivers/MSSQL_drivers_install_debian_8_9.sh')
            run_commands([script])

        elif sys.platform.startswith('darwin'):

            commands = ['/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"',
                        'brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release',
                        'brew update',
                        'brew install --no-sandbox msodbcsql@13.1.9.2 mssql-tools@14.0.6.0']


            pm.print_warning('Make sure you have installed MSSQL Drivers')
            pm.print_separator()
            for c in commands:
                print(c)
            pm.print_separator()

        elif sys.platform.startswith('win'):
            pm.print_warning('Currently, pymake for MSSQL connections is not supported')
