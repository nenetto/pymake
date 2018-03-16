"""
pymake
-------------------------------

pymake package

 - E. Marinetto
 - nenetto@gmail.com
"""
import sys
import json
import pkg_resources
from pprint import pprint
from pymake.utils.project import create_project
from pymake.project_vars import project_vars

# TODO Add support to load projects from private repositories and git support

def main(args=None):
    """Example of entry point"""
    if args is None:
        args = sys.argv[1:]

    """Read the args"""
    if len(args) > 0:
        for i in args:
            print(i)

        create_project(args[0])

    else:
        print('To create a new project, configure your project in a json file as:')
        print('-' * 67)
        pymake_configuration_model = pkg_resources.resource_filename(__name__, 'templates/python_project/pymakeconfigure.json')

        example_conf = json.load(open(pymake_configuration_model))

        pprint(example_conf)
        print('-' * 67)


if __name__ == "__main__":

    logo = pkg_resources.resource_filename(__name__, 'templates/images/logo.txt')

    with open(logo, 'r') as f:
        print(f.read())

    print('\n'*5 + 'Welcome to the project [{0}] created by [{1}]'.format(project_vars['project-name'], project_vars['author']))
    #main()

    create_project('/Users/nenetto/SBD/Ferrovial/datalab/pymake/example/test.json')

