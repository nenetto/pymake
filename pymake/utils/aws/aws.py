"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 16-05-2018
"""

import os


def check_aws_env():

    if ('AWS_KEY_ID' in os.environ) and ('AWS_SECRET_KEY' in os.environ) and ('AWS_REGION_NAME' in os.environ):
        return True
    else:
        return False

