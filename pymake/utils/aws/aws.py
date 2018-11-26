"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 16-05-2018
"""

import os
import boto3
from pymake.utils.common.common_functions import read_env_var


def check_aws_env():

    if ('AWS_KEY_ID' in os.environ) and ('AWS_SECRET_KEY' in os.environ) and ('AWS_REGION_NAME' in os.environ):
        return True
    else:
        return False


def check_aws_env_profile():

    if 'AWS_PROFILE' in os.environ:
        return True
    else:
        return False


def getSession():

    if check_aws_env():
        aws_session = boto3.Session(aws_access_key_id=read_env_var('AWS_KEY_ID'),
                                    aws_secret_access_key=read_env_var('AWS_SECRET_KEY'),
                                    region_name=read_env_var('AWS_REGION_NAME'))
        return aws_session

    elif check_aws_env_profile():
        aws_session = boto3.Session(profile_name=read_env_var('AWS_PROFILE'))
        return aws_session
    else:
        s3 = boto3.Session()

    return s3

