"""
pymake
-------------------------------

pymake package

 - E. Marinetto
 - nenetto@gmail.com
"""
import os
from pymake.project_vars import PrettyMessaging, project_vars
from pymake.utils.pymakeutils import get_pymakevars
from pymake.utils.project_python import create_readme, create_pymake_vars, create_main, create_pymakefile, configure_pymake
from pymake.utils.configuration_parameters import mandatory_parameters_pymakefile
from pymake.utils.pymakeutils import get_value_pymakefile
import tempfile
from pprint import pformat
import shutil


def find_file(path, filepattern):
    PrettyMessaging.print_info('Looking for [{0}] configuration file'.format(filepattern))

    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            abs_path = os.path.join(root, filename)
            relativepath = os.path.relpath(abs_path, path)

            if abs_path[-len(filepattern):] == filepattern:
                PrettyMessaging.print_info('   Found in [{0}]'.format(relativepath))
                return abs_path

    PrettyMessaging.print_error('File [{0}] not found. Please, create your pymake file'.format(filepattern))
    raise ()


def find_pymakefile(path):
    return find_file(path, 'pymakefile.json')


def check_pymakefile(old_pymake):

    pymakevars_old = get_pymakevars(old_pymake, asdict=True)

    for mandatory_var in mandatory_parameters_pymakefile:
        if mandatory_var not in pymakevars_old.keys():
            error_msg = 'Configuration parameter [{0}] was not found in pymakefile'.format(mandatory_var)
            PrettyMessaging.print_error(error_msg)
            raise(ValueError(error_msg))

    PrettyMessaging.print_json(old_pymake)

    PrettyMessaging.print_info('Checking pymake version')
    if 'pymake-version' not in pymakevars_old.keys():
        PrettyMessaging.print_warning('  - Pymake version not found, this feature was introduced in [2.5]')
    else:
        PrettyMessaging.print_info('Pymake version [{0}]'.format(pymakevars_old['pymake-version']))

    PrettyMessaging.print_info('  - Updating pymake to version [{0}.{1}]'.format(project_vars['project-version-major'],
                                                                                 project_vars['project-version-minor']))

    pymakevars_old['pymake-version'] = float('{0}.{1}'.format(project_vars['project-version-major'],
                                                              project_vars['project-version-minor']))

    pymakevars_new_text = pformat(pymakevars_old).replace("'", "\"")
    with open(old_pymake, 'w') as oldf:
        oldf.write(pymakevars_new_text)

    root_path = os.path.abspath(os.path.join(old_pymake, os.pardir))
    create_pymakefile(old_pymake, root_path)

    PrettyMessaging.print_json(old_pymake)

    return pymakevars_old


def find_project_vars(path):

    return find_file(path, 'project_vars.py')


def replace_by_model(old_path, model_path, number_of_lines = None):

    # Rename old version
    old_file = old_path + '_old'
    os.rename(old_path, old_file)

    # Compare and fix old version
    with open(old_file, 'r') as fold, open(model_path, 'r') as fmodel, open(old_path, 'w') as fnew:

        if number_of_lines is None:
            # Replace all
            fnew.write(fmodel.read())
        else:

            # Replace first N lines
            for i in range(number_of_lines):
                fnew.writelines(fmodel.readline())
                fold.readline()

            fnew.write(fold.read())

    os.remove(model_path)
    os.remove(old_file)


def replace_headers(pymakepath, root_path, pname_sp):
    # Replace Headers
    PrettyMessaging.print_info('Revisiting headers')

    header = get_value_pymakefile(pymakepath, 'header') + '\n'

    python_files = []

    for root, directories, filenames in os.walk(root_path):
        for filename in filenames:
            abs_path = os.path.join(root, filename)
            rel_path = os.path.relpath(abs_path, os.path.join(root_path, pname_sp))
            if abs_path[-3:] == '.py' and rel_path[:len('pymake/')] != 'pymake/':
                python_files.append(abs_path)

    # Warnings
    for pfile in python_files:
        rel_path = os.path.relpath(pfile, os.path.join(root_path, pname_sp))
        with open(pfile, 'r') as fp:
            if fp.readline()[:3] != '"""':
                append = True
            else:
                append = False

        if append:

            PrettyMessaging.print_warning('  - [{0}] Appending header, please revise!'.format(rel_path))
            with open(pfile, 'r') as fp:
                text = fp.read()

            ft = tempfile.NamedTemporaryFile('w', delete=False)
            ft.write(header)
            ft.write(text)
            ft.close()

            os.remove(pfile)
            os.rename(ft.name, pfile)

        else:
            PrettyMessaging.print_info('   - [{0}] Updating header'.format(rel_path))

            ft = tempfile.NamedTemporaryFile('w', delete=False)
            ft.write(header)
            ft.close()

            replace_by_model(pfile, ft.name, 9)


def reconfigure_project(input_path):
#if __name__ == "__main__":
#    input_path = '/Users/nenetto/SBD/Ferrovial/pymake_new'

    pymakepath = find_pymakefile(input_path)
    pymakefile_folder = os.path.abspath(os.path.join(pymakepath, os.pardir))
    pymakevars = check_pymakefile(pymakepath)

    # Extract name of project
    pname_sp = pymakevars['project-name'].replace(' ', '_').lower()
    PrettyMessaging.print_info('Starting reconfiguration for project [{0}]'.format(pymakevars['project-name']))

    # Check root directory
    root_path = os.path.abspath(os.path.join(os.path.abspath(os.path.join(pymakepath, os.pardir)), os.pardir))
    PrettyMessaging.print_info('Parent directory: [{0}]'.format(root_path))

    ###############################

    replace_headers(pymakepath, root_path, pname_sp)

    ####################

    PrettyMessaging.print_info('Looking for [setup.py]')
    # If setup.py mark as deleted
    setup_path = os.path.join(root_path, 'setup.py')
    if os.path.isfile(setup_path):
        PrettyMessaging.print_warning('  - [setup.py] found. Generate a new one after reconfigure and make the merge yourself for safety')
        os.rename(setup_path, os.path.join(root_path, 'setup_old.py'))
    else:
        PrettyMessaging.print_info('  - [setup.py] not found. Generate a new one after reconfigure')


#####################

    PrettyMessaging.print_info('Looking for [README.md]')

    # If README.md found, replace header
    old_readme = os.path.join(root_path, 'README.md')
    if os.path.isfile(old_readme):
        PrettyMessaging.print_warning('  - [README.md] found, replacing for new version')

        # Create new version
        model_readme = create_readme(pymakepath, pymakefile_folder, temp=True)
        replace_by_model(old_readme, model_readme, 5)

    else:
        PrettyMessaging.print_warning('  - [README.md] not found, creating new one')
        # Create new version
        create_readme(pymakepath, pymakefile_folder)

    #####################
    PrettyMessaging.print_info('Looking for [project_vars.py]')

    # If project_vars.py found, replace
    project_path = os.path.join(root_path, pname_sp)
    old_file = os.path.join(project_path, 'project_vars.py')
    if os.path.isfile(old_file):
        PrettyMessaging.print_warning('  - [project_vars.py] found, replacing for new version')

        # Create new version
        model_file = create_pymake_vars(pymakepath, pymakefile_folder, temp=True)
        replace_by_model(old_file, model_file)

    else:
        PrettyMessaging.print_warning('  - [project_vars.py] not found, creating new one')
        # Create new version
        create_pymake_vars(pymakepath, pymakefile_folder)

    #####################
    PrettyMessaging.print_info('Looking for [main.py]')

    # If main.py found, replace
    old_file = os.path.join(project_path, 'main.py')
    if os.path.isfile(old_file):
        PrettyMessaging.print_warning('  - [main.py] found, setting a new version and saving old one')

        os.rename(old_file, os.path.join(project_path, 'main_old.py'))

        create_main(pymakepath, pymakefile_folder)

    else:
        PrettyMessaging.print_warning('  - [main.py] not found, creating new one')
        # Create new version
        create_main(pymakepath, pymakefile_folder)


    #####################


    #####################
    PrettyMessaging.print_info('Looking for [pymake]')

    project_path = os.path.join(root_path, pname_sp)
    old_folder = os.path.join(project_path, 'pymake')
    if os.path.isdir(old_folder):
        PrettyMessaging.print_warning('  - [pymake] found, replacing for new version')
        shutil.rmtree(old_folder)

    else:
        PrettyMessaging.print_info('  - [pymake] not found, creating new version')

    configure_pymake(pymakepath, pymakefile_folder)



