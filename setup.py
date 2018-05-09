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
        version='0.1',
        description='',
        long_description=long_description,
        url='https://github.com/nenetto/pymake',
        author='Eugenio Marinetto',
        author_email='nenetto@gmail.com',
        packages=find_packages(),
        install_requires=['tabulate>=0.8.2', 'botocore>=1.9.2', 'pipreqs>=0.4.9', 'setuptools>=38.4.0', 'pandas>=0.22.0', 'psycopg2>=2.7.1', 'boto3>=1.7.16', 'pyodbc>=4.0.23'],
        package_dir={},
        include_package_data=True,
        package_data={'': 'README.md'},
        entry_points={
              'console_scripts': [
                  'pymake = pymake.main:main'
              ]
          }
        )