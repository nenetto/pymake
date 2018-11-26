"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 04-11-2018
"""

from pymake.main import printer as pm
import sagemaker


def get_execution_role(sagemaker_session=None, givenrole=''):
    """
    Returns the role ARN whose credentials are used to call the API.
    In AWS notebook instance, this will return the ARN attributed to the
    notebook. Otherwise, it will return the ARN stored in settings
    at the project level.
    :param: sagemaker_session(Session): Current sagemaker session
    :rtype: string: the role ARN
    """
    try:
        role = sagemaker.get_execution_role(sagemaker_session=sagemaker_session)
    except ValueError as e:
        # read your role from a configuration file, from environment variables, etc. It's up to you
        arn = givenrole.copy()

        if ':role/' in arn:
            role = arn
        else:
            message = 'The current AWS identity is not a role: {},' \
                      'therefore it cannot be used ' \
                      'as a SageMaker execution role'
            raise ValueError(message.format(arn))
    return role

