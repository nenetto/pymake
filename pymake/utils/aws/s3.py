"""
pycharm
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 09-05-2018
"""
import boto3
import botocore
from pymake.utils.common.prettymessaging import PrettyMessaging
import os


def check_aws_env():

    if ('AWS_KEY_ID' in os.environ) and ('AWS_SECRET_KEY' in os.environ) and ('AWS_REGION_NAME' in os.environ):
        return True
    else:
        return False


def s3_resource():
    if check_aws_env():
        aws_session = boto3.Session(aws_access_key_id=os.environ['AWS_KEY_ID'],
                                    aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
                                    region_name=os.environ['AWS_REGION_NAME'])

        s3 = aws_session.resource('s3')
    else:
        s3 = boto3.resource('s3')

    return s3


def upload2s3(file_local_path, s3_bucketname, file_remote_path):

    s3 = s3_resource()
    s3.meta.client.upload_file(file_local_path, s3_bucketname, file_remote_path)


def downloads3(file_local_path, s3_bucketname, file_remote_path, verbose=True):

    pm = PrettyMessaging('pymake')
    s3 = s3_resource()

    if not isfiles3(s3_bucketname, file_remote_path):
        return False

    try:
        s3.Bucket(s3_bucketname).download_file(file_remote_path, file_local_path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            if verbose:
                pm.print_error('[AWS][S3] The object does not exist.')
            return False
        else:
            pm.print_error('[AWS][S3] Unknown error')
            pm.print_error_2(str(e))
            pm.print_error('', exit_code=1)
    return True


def isfiles3(s3_bucketname, file_remote_path):

    s3 = s3_resource()

    result = s3.Bucket(s3_bucketname).Object(file_remote_path)

    exists = False
    if result:
        exists = True

    return exists