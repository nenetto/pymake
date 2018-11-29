"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 16-05-2018
"""

from pymake.utils.sql.database import DataBase
from pymake.main import printer as pm
from pymake.utils.aws.athena import athena_exist, reload_partitions_in_table
from pymake.utils.aws.aws import check_aws_env
import pyathena
import os

class Athena(DataBase):

    def __init__(self, dbname, s3_bucketname, file_remote_path, verbose=True):
        super().__init__(host=None,
                         port=None,
                         dbname=dbname,
                         user=None,
                         pwd=None,
                         verbose=verbose)

        self._s3bucket = s3_bucketname
        self._remotepath = file_remote_path

        self._output_location = 's3://' + '/'.join([self._s3bucket, self._remotepath]) + '/'

    def reload_partition(self, table_name):
        reload_partitions_in_table(self._dbname, table_name, self._s3bucket, self._remotepath)

    def connect(self):

        if not self._connected:

            # Check for database
            if not athena_exist(self._dbname, self._s3bucket, self._remotepath, verbose=False):
                self._connected = False
                pm.print_error('Athena [{0}] does not exist'.format(self._dbname), exit_code=1)

            if check_aws_env():

                try:
                    self._connection = pyathena.connect(aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                                        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                                                        s3_staging_dir=self._output_location,
                                                        region_name=os.environ['AWS_REGION'])

                except Exception as e:
                    pm.print_error('Error connecting to database')
                    pm.print_separator()
                    pm.print_error(str(e))
                    pm.print_separator()
                    self._connected = False


            else:


                try:
                    self._connection = pyathena.connect(s3_staging_dir=self._output_location,
                                                        region_name=os.environ['AWS_REGION'])

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


if __name__ == "__main__":

    athena = Athena('servicios_a_bordo', 'datathena', 'queries')

    query_parameters = {'__PATH__': '5171',
                        '__ORIGIN__': 'VAL',
                        '__DESTINATION__': 'MAA'}

    df = athena.get_query_from_file('/Users/nenetto/work/Ferrovial/ferrovial_servicios_a_bordo/servicios_a_bordo/sql_queries/athena_dated_train.sql',
                                    parameters=query_parameters)

    pm.print_pandas_df(df, 10)


