#parse('header.py')

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='${PROJECT_NAME}',
    version='${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}',
    description='${PROJECT_DESCRIPTION}',
    long_description=long_description,
    url='${GIT_REPOSITORY}',
    author='${AUTHOR}',
    author_email='${AUTHOR_EMAIL}',
    packages=find_packages(),
    include_package_data=True,
    package_data={PACKAGE_DATA},
    install_requires={PACKAGE_REQUIREMENTS},
    entry_points={
          'console_scripts': [
              '{PROJECT_ENTRY_POINT} = {PROJECT_ENTRY_POINT}.main:main'
          ]
      }
)