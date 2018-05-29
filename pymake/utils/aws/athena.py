"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 16-05-2018
"""

import boto3
from pymake.main import printer as pm
from botocore.exceptions import ClientError
from pymake.utils.aws.aws import check_aws_env
from pymake.utils.common.common_functions import read_env_var
import time
import os


def athena_resource():
    if check_aws_env():
        aws_session = boto3.Session(aws_access_key_id=read_env_var('AWS_KEY_ID'),
                                    aws_secret_access_key=read_env_var('AWS_SECRET_KEY'),
                                    region_name=read_env_var('AWS_REGION_NAME'))

        athena = aws_session.client('athena')
    else:
        athena = boto3.client('athena', region_name=read_env_var('AWS_REGION_NAME'))

    return athena


def athena_query(query, athena_database, s3_bucketname, file_remote_path, verbose=True):

    athena = athena_resource()
    output_location = 's3://' + '/'.join([s3_bucketname, file_remote_path]) + '/'

    query_result = None
    response = None

    try:
        response = athena.start_query_execution(QueryString=query,
                                                QueryExecutionContext={'Database': athena_database},
                                                ResultConfiguration={'OutputLocation': output_location,
                                                                     'EncryptionConfiguration': {
                                                                         'EncryptionOption': 'SSE_S3'}
                                                                     }
                                                )

    except ClientError as err:
        pm.print_warning('Athena [{0}] error'.format(athena_database))
        pm.print_error(err.response['Error']['Message'], exit_code=1)

    try:

        while True:
            status = athena.get_query_execution(QueryExecutionId=response['QueryExecutionId'])
            current_status = status['QueryExecution']['Status']['State']

            if current_status not in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                if verbose:
                    pm.print_info_flush(msg='Query Status: {0}'.format(current_status), wait=True)
            elif current_status == 'SUCCEEDED':
                if verbose:
                    pm.print_info_flush(msg='Query Status: {0}'.format(current_status), wait=False)
                query_result = athena.get_query_results(QueryExecutionId=response['QueryExecutionId'])
                break
            else:
                if verbose:
                    pm.print_error('Query {0}'.format(current_status))
                return None

    except ClientError as err:
        pm.print_warning('Athena [{0}] error'.format(athena_database))
        pm.print_error(err.response['Error']['Message'], exit_code=1)

    return query_result


def athena_exist(athena_database, s3_bucketname, file_remote_path, verbose=True):

    query = 'SHOW TABLES IN {0};'.format(athena_database)

    query_result = athena_query(query, athena_database, s3_bucketname, file_remote_path, verbose)

    if query_result is not None:
        return True
    else:
        return False


def reload_partitions_in_table(athena_database, athena_table, s3_bucketname, file_remote_path, verbose=True):

    if not athena_exist(athena_database, s3_bucketname, file_remote_path, False):
        pm.print_error('Database does not exist', exit_code=1)

    athena = athena_resource()

    output_location = 's3://' + '/'.join([s3_bucketname, file_remote_path]) + '/'

    response = None

    try:
        response = athena.start_query_execution(QueryString='MSCK REPAIR TABLE {0};'.format(athena_table),
                                                QueryExecutionContext={'Database': athena_database},
                                                ResultConfiguration={'OutputLocation': output_location,
                                                                     'EncryptionConfiguration': {
                                                                         'EncryptionOption': 'SSE_S3'}
                                                                     }
                                                )
    except ClientError as err:
        pm.print_error('Reload partitions failed on table [{0}.{1}]'.format(athena_database, athena_table))
        pm.print_error(err.response['Error']['Message'], exit_code=1)

    try:

        while True:
            status = athena.get_query_execution(QueryExecutionId=response['QueryExecutionId'])
            current_status = status['QueryExecution']['Status']['State']

            if current_status not in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                if verbose:
                    pm.print_info_flush(msg='Query Status: {0}'.format(current_status), wait=True)
            elif current_status == 'SUCCEEDED':
                if verbose:
                    pm.print_info_flush(msg='Query Status: {0}'.format(current_status), wait=False)
                _ = athena.get_query_results(QueryExecutionId=response['QueryExecutionId'])
                break
            else:
                if verbose:
                    pm.print_error('Query {0}'.format(current_status))
                return None
            time.sleep(5)

    except ClientError as err:
        pm.print_warning('Athena [{0}] error'.format(athena_database))
        pm.print_error(err.response['Error']['Message'], exit_code=1)
    else:
        pm.print_info('Reload partitions succeed on table [{0}.{1}]'.format(athena_database, athena_table))
