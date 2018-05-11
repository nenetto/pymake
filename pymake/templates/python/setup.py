"""
${PROJECT_NAME}
-------------------------------
 - ${AUTHOR}
 - ${AUTHOR_EMAIL}
-------------------------------
"""

from setuptools import setup, find_packages
from setuptools.command.install import install
from codecs import open
from os import path
import pkg_resources

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def pre_post_decorator(command_subclass):
    """A decorator for classes subclassing one of the setuptools commands.

    It modifies the run() method so that allow to do something else.
    """
    orig_run = command_subclass.run

    def modified_run(self):

        ## Insert pre install here

        orig_run(self)

        ## Insert post install here

    command_subclass.run = modified_run
    return command_subclass


@pre_post_decorator
class CustomInstallCommand(install):
    pass


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