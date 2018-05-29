"""
pymake
-------------------------------
 - Rafael Álvarez
-------------------------------
Created 29-05-2018
"""

import boto3
from pymake.main import printer as pm
from botocore.exceptions import ClientError
from pymake.utils.aws.aws import check_aws_env
from pymake.utils.common.common_functions import read_env_var
import os


def sns_resource():
    if check_aws_env():
        aws_session = boto3.Session(aws_access_key_id=read_env_var('AWS_KEY_ID'),
                                    aws_secret_access_key=read_env_var('AWS_SECRET_KEY'),
                                    region_name=read_env_var('AWS_REGION_NAME'))

        sns = aws_session.client('sns')
    else:
        sns = boto3.client('sns', region_name=read_env_var('AWS_REGION_NAME'))

    return sns


def sns_publish(topic, message):

    sns = sns_resource()   

    try:
        response = sns.publish(TopicArn = topic, Message = message)

    except ClientError as err:
        pm.print_warning('SNS [{0}] error')
        pm.print_error(err.response['Error']['Message'], exit_code=1)    

    return response
