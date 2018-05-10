"""
${PROJECT_NAME}
-------------------------------
 - ${AUTHOR}
 - ${AUTHOR_EMAIL}
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
        name='${PROJECT_NAME}',
        version='${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}',
        description='${PROJECT_DESCRIPTION}',
        long_description=long_description,
        url='${GIT_REPOSITORY}',
        author='${AUTHOR}',
        author_email='${AUTHOR_EMAIL}',
        packages=find_packages(exclude=("tests",)),
        install_requires='${PACKAGE_REQUIREMENTS}',
        include_package_data=True,
        package_data='${PACKAGE_DATA}',
        entry_points={'console_scripts': ['${PROJECT_NAME} = ${PROJECT_NAME}.main:main']}
        )