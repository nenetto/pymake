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
from pymake.utils.aws.aws import getSession


def insert_dynamo(table_name, dict_data, key_name, force=True):
    aws_session = getSession()
    dynamo = aws_session.client('dynamodb')

    try:
        _ = dynamo.put_item(TableName=table_name,
                            Item=dict_data,
                            ReturnConsumedCapacity='TOTAL',
                            ConditionExpression='attribute_not_exists({0})'.format(key_name))

    except botocore.exceptions.ClientError as e:

        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':

            if force:
                pm.print_info('Forcing to rewrite [{0}:{1}]'.format(key_name, dict_data[key_name]))
                pm.print_dict(dict_data)

                _ = dynamo.put_item(TableName=table_name,
                                    Item=dict_data,
                                    ReturnConsumedCapacity='TOTAL')

            else:
                pm.print_warning('Key already exists [{0}:{1}]'.format(key_name, dict_data[key_name]))

        else:
            pm.print_error('Dynamo problem unknown')
            pm.print_error(str(e), exit_code=1)
