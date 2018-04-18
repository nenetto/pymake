from pymake.utils import pymakeutils, project_python, project_r
from pymake.project_vars import PrettyMessaging


def create_project(pymakeconfigure):

    # Extract name of project
    pname = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=False)
    type_of_project = pymakeutils.get_value_pymakefile(pymakeconfigure, 'type_of_project', mandatory=True,
                                                       default='python')

    if type_of_project in pymakeutils.supported_project_types:
        PrettyMessaging.print_info('Creating project of type [{1}] '.format(pname, type_of_project))

        if type_of_project == 'python':
            project_python.create_project(pymakeconfigure)

        if type_of_project == 'R':
            project_r.create_project(pymakeconfigure)

    else:
        msg = 'Type of project [{0}] not supported :D, what about creating yourself?'.format(type_of_project)
        PrettyMessaging.print_error(msg)
        raise(ValueError(msg))

