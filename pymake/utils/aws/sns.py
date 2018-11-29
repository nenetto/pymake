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
from pymake.utils.aws.aws import getSession
from pymake.utils.aws.aws import check_aws_env, check_aws_env_profile
from pymake.utils.common.common_functions import read_env_var
import os


def sns_resource():
    aws_session = getSession()
    sns = aws_session.client('sns')
    return sns


def sns_publish(topic, message):

    sns = sns_resource()   

    try:
        response = sns.publish(TopicArn = topic, Message = message)

    except ClientError as err:
        pm.print_warning('SNS [{0}] error')
        pm.print_error(err.response['Error']['Message'], exit_code=1)    

    return response
