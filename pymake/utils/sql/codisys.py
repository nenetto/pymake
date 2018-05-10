import pyodbc
from pymake.utils.sql.database import DataBase
from pymake.utils.common.common_functions import read_env_var

'''

https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server#os-x-1011-el-capitan-and-macos-1012-sierra

Important step to make pypyodbc works on OSX

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install --no-sandbox msodbcsql@13.1.9.2 mssql-tools@14.0.6.0

pip install pyodbc
'''


class Codisys(DataBase):

    def __init__(self, verbose=True):
        super().__init__()

        self._connection = None
        self._connected = False
        self._verbose = verbose

        # CODISYS connection info
        self._host = read_env_var('CODISYS_HOST')
        self._port = read_env_var('CODISYS_PORT')
        self._dbname = read_env_var('CODISYS_DB_NAME')
        self._user = read_env_var('CODISYS_USER')
        self._pwd = read_env_var('CODISYS_PWD')

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
                self.pm.print_error('go to-> https://docs.microsoft.com/en-us/sql/connect/odbc/\
                                    linux-mac/installing-the-microsoft-odbc-driver-for-sql-server#os-x-1011-el\
                                    -capitan-and-macos-1012-sierra')
                self.pm.print_separator()
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
