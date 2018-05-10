"""
pymake
-------------------------------

pymake package

 - E. Marinetto
 - nenetto@gmail.com
"""
import os
import subprocess
import pipreqs
from pprint import pformat
import pkg_resources
from setuptools import find_packages
from pymake.utils.common.prettymessaging import PrettyMessaging
from pymake.utils.common.common_functions import json2dict


def isignored(f_path):

    if f_path[0] == '.':
        return True

    if '__pycache__' in f_path:
        return True

    if '.git' in f_path:
        return True

    f_name = os.path.split(f_path)[-1]

    if f_name[-4:] in ['.pyc']:
        return True

    if f_name[0] == '.':
        return True

    else:
        return False


def find_pymakefile(path):
    pm = PrettyMessaging('pymake')

    tested_names = ['Pymakefile.json',
                    'Pymakefile',
                    'pymakefile.json',
                    'pymakefile',
                    'Pymake.json',
                    'Pymake',
                    'pymake.json',
                    'pymake']

    for t in tested_names:
        abs_path = os.path.join(path, t)
        if os.path.isfile(abs_path):
            pm.print_info('[Pymakefile] found @ {0}'.format(abs_path))
            return abs_path

    pm.print_error('Pymakefile not found')
    pm.print_error('  - Please, use one of the accepted names')
    for t in tested_names:
        pm.print_error('  - [{0}]'.format(t))
    pm.print_error('', exit_code=1)


def find_main_packages_folder(path):
    packages = find_packages(path)
    packages_folders = list()

    for p in packages:
        folders = p.split('.')

        if len(folders) == 1:
            packages_folders.append(p)
        else:
            # packages_folders.append(reduce(os.path.join, folders))
            pass

    return packages_folders


def create_setup(path):

    pm = PrettyMessaging('pymake')
    pm.print_info('Creating setup.py')

    package_path = path

    pm.print_info('Looking for Pymakefile')
    pymake_path = find_pymakefile(path)
    pymakevars = json2dict(pymake_path)

    pm.print_separator()
    pm.print_info('Configuring setup for project [{0}]'.format(pymakevars['PROJECT_NAME']))

    # Create setup.py
    pm.print_info('Generating setup.py')

    setup_file_path = os.path.join(path, 'setup.py')
    if os.path.exists(setup_file_path) and os.path.isfile(setup_file_path):
        pm.print_warning('Deleting old setup.py [{0}]'.format(setup_file_path))
        os.rename(setup_file_path, setup_file_path[:-3] + '_old.py')

    # Configuring requirements data
    # Create requirements file using pipreqs

    fnull = open(os.devnull, 'w')
    pm.print_info('Looking for requirements with pipreqs v{0}'.format(pipreqs.__version__))
    subprocess.check_call(['pipreqs', '--force', '--ignore', 'templates', '{0}'.format(path)],
                          stdout=fnull,
                          stderr=fnull)
    requirements_file_path = os.path.join(package_path, 'requirements.txt')

    requirements = []
    with open(requirements_file_path, 'r') as f:
        content = f.readlines()

    content = [x.strip().replace('==', '>=') for x in content]
    if content != ['']:
        requirements = requirements + content

    for r in requirements:
        pm.print_info('   - [{0}]'.format(r))

    # Delete requirements file
    os.remove(requirements_file_path)

    # Configuring Package data
    pm.print_info('Looking for resources')

    packages_folders = find_main_packages_folder(path)
    package_data_list = []

    for p in packages_folders:

        for root, directories, filenames in os.walk(os.path.join(path, p)):
            for filename in filenames:
                abs_path = os.path.join(root, filename)
                common_prefix = os.path.commonprefix([os.path.join(path, p), abs_path])
                path2add = os.path.relpath(abs_path, common_prefix)

                if not isignored(path2add):
                    package_data_list.append(path2add)
                    pm.print_info('   - [{0}]'.format(os.path.split(path2add)[-1]))

    package_data = {'': package_data_list}

    setup_template = pkg_resources.resource_filename('pymake', 'templates/python/setup.py')

    # Replacing variables
    pm.print_info('Reading template setup.py')
    with open(setup_template, 'r') as setup_file:
        setup_text = setup_file.read()

    pm.print_info('Setting variables setup.py')

    setup_text = setup_text.replace('${PROJECT_NAME}', pymakevars['PROJECT_NAME'])
    setup_text = setup_text.replace('${PROJECT_VERSION_MAJOR}', pymakevars['PROJECT_VERSION_MAJOR'])
    setup_text = setup_text.replace('${PROJECT_VERSION_MINOR}', pymakevars['PROJECT_VERSION_MINOR'])
    setup_text = setup_text.replace('${PROJECT_DESCRIPTION}', pymakevars['PROJECT_DESCRIPTION'])
    setup_text = setup_text.replace('${GIT_REPOSITORY}', pymakevars['GIT_REPOSITORY'])
    setup_text = setup_text.replace('${AUTHOR}', pymakevars['AUTHOR'])
    setup_text = setup_text.replace('${AUTHOR_EMAIL}', pymakevars['AUTHOR_EMAIL'])
    setup_text = setup_text.replace('${PROJECT_NAME}', pymakevars['PROJECT_NAME'])
    setup_text = setup_text.replace('\'${PACKAGE_REQUIREMENTS}\'', str(requirements))
    setup_text = setup_text.replace('\'${PACKAGE_DATA}\'', pformat(package_data))

    pm.print_info('Saving setup.py')

    with open(setup_file_path, 'w') as setup_file:
        setup_file.write(setup_text)

    pm.print_info('Setup.py created successfully')
    pm.print_separator()
