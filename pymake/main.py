"""
pymake
-------------------------------

pymake package

 - E. Marinetto
 - nenetto@gmail.com
"""
import sys
import pkg_resources
from pymake.utils.project import create_project
from pymake.project_vars import project_vars, PrettyMessaging
from pymake.utils.reconfigure import reconfigure_project


def main(args=None):
    """Example of entry point"""
    if args is None:
        args = sys.argv[1:]

    """Read the args"""
    if len(args) > 0:

        if args[0] == '-configure':
            create_project(args[1])

        if args[0] == '-reconfigure':
            reconfigure_project(args[1])

    else:
        PrettyMessaging.print_warning('To create a new project, configure your project in a json file as:')
        pymake_configuration_model = pkg_resources.resource_filename(__name__, 'templates/python_project/pymakeconfigure.json')
        PrettyMessaging.print_json(pymake_configuration_model)


if __name__ == "__main__":

    PrettyMessaging.print_info('Welcome to the project [{0}] created by [{1}]'.format(project_vars['project-name'], project_vars['author']))
    main()
