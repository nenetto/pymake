"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='pymake',
        version='0.3',
        description='',
        long_description=long_description,
        url='https://github.com/nenetto/pymake',
        author='Eugenio Marinetto',
        author_email='nenetto@gmail.com',
        packages=find_packages(exclude=("tests",)),
        install_requires=['pipreqs>=0.4.9', 'psycopg2>=2.7.4', 'pandas>=0.22.0', 'tabulate>=0.8.2', 'setuptools>=39.1.0', 'botocore>=1.10.16', 'boto3>=1.7.16', 'pyodbc>=4.0.23'],
        include_package_data=True,
        package_data={'': ['__init__.py',
      'main.py',
      'tools/__init__.py',
      'tools/create_setup.py',
      'to_refactor/test_utils_common_functions.py',
      'to_refactor/create_docker_image.py',
      'tests/__init__.py',
      'tests/utils/test_utils_prettymessaging.py',
      'tests/utils/__init__.py',
      'utils/__init__.py',
      'utils/common/prettymessaging.py',
      'utils/common/__init__.py',
      'utils/common/common_functions.py',
      'utils/common/text_modifiers.py',
      'utils/aws/__init__.py',
      'utils/aws/s3.py',
      'utils/sql/database.py',
      'utils/sql/__init__.py',
      'utils/sql/zitycar.py',
      'utils/sql/codisys.py',
      'recipes/docker/aws_resources/configure_aws_cli.sh',
      'recipes/docker/MSSQL_drivers/MSSQL_drivers_install_debian_8_9.sh',
      'recipes/docker/forticlient_vpn/forticlient.sh',
      'recipes/docker/forticlient_vpn/forticlient_setup',
      'recipes/docker/forticlient_vpn/forticlient_docker_install_debian8.sh',
      'recipes/docker/forticlient_vpn/connect_vpn.sh',
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