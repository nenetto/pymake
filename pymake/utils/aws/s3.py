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
from pymake.main import printer as pm
from pymake.utils.aws.aws import getSession


def s3_resource():
    aws_session = getSession()
    s3 = aws_session.resource('s3')

    return s3


def upload2s3(file_local_path, s3_bucketname, file_remote_path):

    s3 = s3_resource()
    s3.meta.client.upload_file(file_local_path, s3_bucketname, file_remote_path)
    s3 = None


def downloads3(file_local_path, s3_bucketname, file_remote_path, verbose=True):

    s3 = s3_resource()

    if not isfiles3(s3_bucketname, file_remote_path):
        s3 = None
        return False

    try:
        s3.Bucket(s3_bucketname).download_file(file_remote_path, file_local_path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            if verbose:
                pm.print_error('[AWS][S3] The object does not exist.')
            s3 = None
            return False
        else:
            pm.print_error('[AWS][S3] Unknown error')
            pm.print_error_2(str(e))
            s3 = None
            pm.print_error('', exit_code=1)

    s3 = None
    return True


def isfiles3(s3_bucketname, file_remote_path):

    s3 = s3_resource()

    try:
        s3.Object(s3_bucketname, file_remote_path).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            s3 = None
            return False
        else:
            # Something else has gone wrong.
            s3 = None
            pm.print_error('[AWS][S3] Unknown error')
            pm.print_error(str(e))
            pm.print_error('', exit_code=1)
    else:
        s3 = None
        return True


def deletes3(s3_bucketname, file_remote_path):

    if isfiles3(s3_bucketname, file_remote_path):
        s3 = s3_resource()

        try:
            s3.Object(s3_bucketname, file_remote_path).delete()
        except botocore.exceptions.ClientError as e:
            # Something else has gone wrong.
            s3 = None
            pm.print_error('[AWS][S3] Unknown error')
            pm.print_error(str(e))
            pm.print_error('', exit_code=1)
        else:
            s3 = None
            return True

    else:
        pm.print_warning('File [s3://{0}/{1}] does not exist'.format(s3_bucketname, file_remote_path))