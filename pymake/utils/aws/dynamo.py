"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 04-09-2018
"""

import boto3
import botocore
import botocore.exceptions
from pymake.main import printer as pm
from pymake.utils.aws.aws import check_aws_env
from pymake.utils.common.common_functions import read_env_var


def insert_dynamo(table_name, dict_data, key_name, force=True):

    if check_aws_env():

        aws_session = boto3.Session(aws_access_key_id=read_env_var('AWS_KEY_ID'),
                                    aws_secret_access_key=read_env_var('AWS_SECRET_KEY'),
                                    region_name=read_env_var('AWS_REGION_NAME'))

        dynamo = aws_session.client('dynamodb')

    else:
        dynamo = boto3.client('dynamodb', region_name=read_env_var('AWS_REGION_NAME'))

    try:
        _ = dynamo.put_item(TableName=table_name,
                            Item=dict_data,
                            ReturnConsumedCapacity='TOTAL',
                            ConditionExpression='attribute_not_exists({0})'.format(key_name))

    except botocore.exceptions.ClientError as e:

        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':

            if force:
                pm.print_info('Forcing to rewrite [{0}:{1}]'.format(key_name, dict_data[key_name]))

                _ = dynamo.put_item(TableName=table_name,
                                    Item=dict_data,
                                    ReturnConsumedCapacity='TOTAL')

            else:
                pm.print_warning('Key already exists [{0}:{1}]'.format(key_name, dict_data[key_name]))

        else:
            pm.print_error('Dynamo problem unknown')
            pm.print_error(str(e), exit_code=1)
