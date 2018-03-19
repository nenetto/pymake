"""
pymake
-------------------------------

pymake package

 - E. Marinetto
 - nenetto@gmail.com
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
    version='2.0',
    description='pymake package',
    long_description=long_description,
    url='https://github.com/nenetto/pymake.git',
    author='E. Marinetto',
    author_email='nenetto@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': [ 'pymakefile.json',
                        'templates/python_package/__init__.template',
                        'templates/images/logo.txt',
                        'templates/python_project/header.template',
                        'templates/python_project/pymakefile.template',
                        'templates/python_project/README.template',
                        'templates/python_project/__init__.template',
                        'templates/python_project/pymake_vars.template',
                        'templates/python_project/main.template',
                        'templates/python_project/pymakeconfigure.json',
                        'templates/pymake/gitignore.template',
                        'templates/pymake/docker_python/aws_push.template',
                        'templates/pymake/docker_python/dockerignore.template',
                        'templates/pymake/docker_python/create_image.template',
                        'templates/pymake/docker_python/run_container_local.template',
                        'templates/pymake/docker_python/Dockerfile.template',
                        'templates/pymake/docker_python/create_docker_image.template',
                        'templates/pymake/docker_R/aws_push.template',
                        'templates/pymake/docker_R/create_docker_image.template',
                        'templates/pymake/docker_R/create_image.template',
                        'templates/pymake/docker_R/Dockerfile.template',
                        'templates/pymake/docker_R/dockerignore.template',
                        'templates/pymake/docker_R/install_package_command.template',
                        'templates/pymake/docker_R/install_R_dependencies.template',
                        'templates/pymake/docker_R/main.template',
                        'templates/pymake/docker_R/run_container_local.template',
                        'templates/R_project/gitignore.template',
                        'templates/R_project/header.template',
                        'templates/R_project/main.template',
                        'templates/R_project/pymake_vars.template',
                        'templates/R_project/pymakefile.template',
                        'templates/R_project/README.template',
                        'templates/R_project/RPoject.template',
                        'templates/pymake/setup/setup.template',
                        'templates/pymake/setup/create_setup.template']},
    install_requires=['setuptools==38.4.0', 'pipreqs==0.4.9'],
    entry_points={
          'console_scripts': [
              'pymake = pymake.main:main'
          ]
      }
)