import pyodbc
from datalab_utils.sql.database import DataBase
import warnings
from datalab_utils.project_vars import PrettyMessaging

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
        self._host = '192.168.0.3'
        self._port = 1433
        self._dbname = 'CODYSHOP'
        self._user = 'codisys'
        self._pwd = "P@ssw0rd1"

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
                PrettyMessaging.print_error('[Codisys]: Error connecting to database')
                PrettyMessaging.print_error('[Codisys]: Did you install MSSQL drivers?')
                PrettyMessaging.print_error('[Codisys]:    go to-> https://docs.microsoft.com/en-us/sql/connect/odbc/\
                                             linux-mac/installing-the-microsoft-odbc-driver-for-sql-server#os-x-1011-el\
                                             -capitan-and-macos-1012-sierra')
                PrettyMessaging.print_separator()
                PrettyMessaging.print_error(str(e))
                PrettyMessaging.print_separator()
                self._connected = False
                return

            self._connected = True

            if self._verbose:
                PrettyMessaging.print_info('[Codisys]: Connection Success')

    def disconnect(self):
        if self._connected:
            self._connection.close()
            self._connected = False
            if self._verbose:
                PrettyMessaging.print_info('[Codisys]: Disconnection Success')
