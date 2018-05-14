"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
"""

from setuptools import setup, find_packages
from codecs import open
from os import path
import sys


here = path.abspath(path.dirname(__file__))

# PRE INSTALL COMMANDS COMES HERE
sys.path.append(here)
from pymake.presetup import preinstall
preinstall()


# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
        name='pymake',
        version='0.7',
        description='',
        long_description=long_description,
        url='https://github.com/nenetto/pymake',
        author='Eugenio Marinetto',
        author_email='nenetto@gmail.com',
        packages=find_packages(exclude=("tests",)),
        install_requires=['tabulate>=0.8.2', 'pyodbc>=4.0.23', 'setuptools>=38.4.0', 'pipreqs>=0.4.9', 'psycopg2>=2.7.1', 'boto3>=1.7.16', 'pexpect>=4.3.0', 'pandas>=0.22.0', 'botocore>=1.10.16'],
        include_package_data=True,
        package_data={'': ['presetup.py',
      '__init__.py',
      'main.py',
      'tools/__init__.py',
      'tools/create_setup.py',
      'to_refactor/test_utils_common_functions.py',
      'to_refactor/create_docker_image.py',
      'utils/__init__.py',
      'utils/docker/__init__.py',
      'utils/docker/docker.py',
      'utils/vpn/__init__.py',
      'utils/vpn/forticlient.py',
      'utils/vpn/forticlient/forticlient.sh',
      'utils/vpn/forticlient/forticlient_setup',
      'utils/vpn/forticlient/forticlient_docker_install_debian8.sh',
      'utils/vpn/forticlient/connect_vpn.sh',
      'utils/common/prettymessaging.py',
      'utils/common/scripting.py',
      'utils/common/__init__.py',
      'utils/common/common_functions.py',
      'utils/common/text_modifiers.py',
      'utils/aws/__init__.py',
      'utils/aws/s3.py',
      'utils/sql/postgress.py',
      'utils/sql/mssql.py',
      'utils/sql/database.py',
      'utils/sql/__init__.py',
      'utils/sql/MSSQL_drivers/MSSQL_drivers_install_debian_8_9.sh',
      'recipes/docker/aws_resources/configure_aws_cli.sh',
      'templates/docker/python/aws_push.sh',
      'templates/docker/python/create_image.sh',
      'templates/docker/python/Dockerfile.sh',
      'templates/docker/python/dockerignore',
      'templates/docker/python/run_container_local.sh',
      'templates/docker/R/install_R_dependencies.template',
      'templates/docker/R/create_docker_image.template',
      'templates/docker/R/aws_push.template',
      'templates/docker/R/dockerignore.template',
      'templates/docker/R/create_image.template',
      'templates/docker/R/install_package_command.template',
      'templates/docker/R/run_container_local.template',
      'templates/docker/R/Dockerfile.template',
      'templates/docker/R/main.template',
      'templates/python/__init__.py',
      'templates/python/setup.py',
      'templates/python/module.py',
      'templates/python/main.py',
      'templates/python/python_header',
      'templates/general/README.md',
      'templates/general/header',
      'templates/R/RProject.template',
      'templates/R/gitignore.template',
      'templates/R/header.template',
      'templates/R/pymakefile.template',
      'templates/R/README.template',
      'templates/R/pymake_vars.template',
      'templates/R/main.template',
      'templates/bash/bash_header']},
        entry_points={'console_scripts': ['pymake = pymake.main:main']}
        )