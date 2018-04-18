import pkg_resources
import os
import shutil
from pymake.utils import pymakeutils
from pymake.project_vars import PrettyMessaging

def create_readme(pymakeconfigure, root_path):

    # Read README.md template file
    readme = pkg_resources.resource_filename('pymake', 'templates/python_project/README.template')
    readme = pymakeutils.replace_template(readme, pymakeconfigure)

    file_path = os.path.join(os.path.dirname(root_path), 'README.md')

    with open(file_path, 'w') as f:
        f.write(readme)


def create_init(pymakeconfigure, root_path):

    # Read package __init__.py template file
    project_init = pkg_resources.resource_filename('pymake', 'templates/python_project/__init__.template')
    project_init = pymakeutils.replace_template(project_init, pymakeconfigure, mandatory=False)

    # Replace package_imports
    packages = pymakeutils.get_value_pymakeconfigure(pymakeconfigure, 'packages', mandatory=False)
    package_imports = ''
    for pack, conf in packages.items():
        package_imports += '#from {0} import [MODULE] as [MODULE]\n'.format(pack)

    project_init = project_init.replace('{package_imports}', package_imports)

    file_path = os.path.join(root_path, '__init__.py')
    with open(file_path, 'w') as f:
        f.write(project_init)


def create_main(pymakeconfigure, root_path):

    # Read package __init__.py template file
    project_init = pkg_resources.resource_filename('pymake', 'templates/python_project/main.template')
    project_init = pymakeutils.replace_template(project_init, pymakeconfigure, mandatory=False)

    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()

    project_init = project_init.replace('{project_name_package}', pname_sp)

    file_path = os.path.join(root_path, 'main.py')

    with open(file_path, 'w') as f:
        f.write(project_init)


def create_pymake_vars(pymakefile, root_path):

    # Read package vars.py template file
    project_vars = pkg_resources.resource_filename('pymake', 'templates/python_project/pymake_vars.template')
    project_vars = pymakeutils.replace_template(project_vars, pymakefile)

    file_path = os.path.join(root_path, 'project_vars.py')

    with open(file_path, 'w') as f:
        f.write(project_vars)


def create_pymakefile(pymakeconfigure, root_path):

    # Read package vars.py template file
    project_vars = pkg_resources.resource_filename('pymake', 'templates/python_project/pymakefile.template')
    project_vars = pymakeutils.replace_template(project_vars, pymakeconfigure)

    file_path = os.path.join(root_path, 'pymakefile.json')

    with open(file_path, 'w') as f:
        f.write(project_vars)


def create_packages(pymakeconfigure, root_path):
    # Extract name of project
    pname = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=False)
    PrettyMessaging.print_info('Creating packages')

    # Read package __init__.py template file
    project_init = pkg_resources.resource_filename('pymake', 'templates/python_package/__init__.template')
    project_init = pymakeutils.replace_template(project_init, pymakeconfigure)

    packages = pymakeutils.get_value_pymakeconfigure(pymakeconfigure, 'packages', mandatory=False)
    for pack, conf in packages.items():
        PrettyMessaging.print_info('   - [{0}]'.format(pack))

        pack_path = os.path.join(root_path, pack)
        os.makedirs(pack_path)

        file_path = os.path.join(pack_path, '__init__.py')
        with open(file_path, 'w') as f:
            f.write(project_init)


def configure_pymake(pymakeconfigure, root_path):

    # Create pymake dir
    PrettyMessaging.print_info('Configuring pymake')
    pymake_path = os.path.join(root_path, 'pymake')
    os.makedirs(pymake_path)

    # Create folder setup
    setup_path = os.path.join(pymake_path, 'setup')
    os.makedirs(setup_path)

    # Setup.py
    PrettyMessaging.print_info('Setup:')
    PrettyMessaging.print_info('   - setup.template')
    setup_file = pkg_resources.resource_filename('pymake', 'templates/pymake/setup/setup.template')
    setup_file = pymakeutils.replace_template(setup_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(setup_path, 'setup.py.template')

    with open(file_path, 'w') as f:
        f.write(setup_file)

    # create_setup.py
    PrettyMessaging.print_info('   - create_setup.py')
    create_setup_file = pkg_resources.resource_filename('pymake', 'templates/pymake/setup/create_setup.template')
    create_setup_file = pymakeutils.replace_template(create_setup_file, pymakeconfigure, mandatory=False)

    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()
    create_setup_file = create_setup_file.replace('{project_name_package}', pname_sp)

    file_path = os.path.join(setup_path, 'create_setup.py')

    with open(file_path, 'w') as f:
        f.write(create_setup_file)

    # Create folder docker
    PrettyMessaging.print_info('Docker:')
    docker_path = os.path.join(pymake_path, 'docker')
    os.makedirs(docker_path)

    # Dockerfile
    PrettyMessaging.print_info('   - Dockerfile')
    dockerfile_file = pkg_resources.resource_filename('pymake', 'templates/pymake/docker_python/Dockerfile.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'Dockerfile.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # run_container_local
    PrettyMessaging.print_info('   - run_container_local.sh')
    dockerfile_file = pkg_resources.resource_filename('pymake', 'templates/pymake/docker_python/run_container_local.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'run_container_local.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # create_image
    PrettyMessaging.print_info('   - create_image.sh')
    dockerfile_file = pkg_resources.resource_filename('pymake',
                                                      'templates/pymake/docker_python/create_image.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'create_image.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # aws_push
    PrettyMessaging.print_info('   - aws_push.sh')
    dockerfile_file = pkg_resources.resource_filename('pymake',
                                                      'templates/pymake/docker_python/aws_push.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'aws_push.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # .dockerignore
    PrettyMessaging.print_info('   - .dockerignore')
    dockerfile_file = pkg_resources.resource_filename('pymake',
                                                      'templates/pymake/docker_python/dockerignore.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'dockerignore.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # create_docker_image.py
    PrettyMessaging.print_info('   - create_docker_image.py')
    dockerfile_file = pkg_resources.resource_filename('pymake', 'templates/pymake/docker_python/create_docker_image.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()
    dockerfile_file = dockerfile_file.replace('{project_name_package}', pname_sp)

    file_path = os.path.join(docker_path, 'create_docker_image.py')

    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # Copy docker utils
    PrettyMessaging.print_info('Docker Utils')

    docker_utils_path = pkg_resources.resource_filename('pymake', 'templates/pymake/docker_utils')
    shutil.copytree(docker_utils_path, os.path.join(docker_path, 'docker_utils'))


def create_resources(pymakeconfigure, root_path):
    # Extract name of project
    PrettyMessaging.print_info('Creating resources')
    resources = pymakeutils.get_value_pymakeconfigure(pymakeconfigure, 'resource-folders', mandatory=False)

    for resource in resources:
        PrettyMessaging.print_info('  - [{0}]'.format(resource))

        pack_path = os.path.join(root_path, resource)
        os.makedirs(pack_path)


def create_default_files(pymakeconfigure, root_path):
    PrettyMessaging.print_info('Configuring files')

    # pymakefile.json
    PrettyMessaging.print_info('   - pymakefile.json')
    create_pymakefile(pymakeconfigure, root_path)
    pymakefile = os.path.join(root_path, 'pymakefile.json')

    # pymake_vars.py
    PrettyMessaging.print_info('   - pymake_vars.py')
    create_pymake_vars(pymakefile, root_path)

    # README.md
    PrettyMessaging.print_info('   - README.py')
    create_readme(pymakeconfigure, root_path)

    # __init__.py
    PrettyMessaging.print_info('   - __init__.py')
    create_init(pymakeconfigure, root_path)

    # main.py
    PrettyMessaging.print_info('   - main.py')
    create_main(pymakeconfigure, root_path)

    # pymakeconfiguration.json
    shutil.copy(pymakeconfigure, os.path.join(os.path.dirname(root_path), 'pymakeconfigure.json'))


def create_project(pymakeconfigure):

    # Extract name of project
    pname = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=False)
    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()


    # Extract directory root
    root_path = os.path.join(pymakeutils.get_value_pymakeconfigure(pymakeconfigure, 'parent-folder'))

    # Check if exists
    if not os.path.isdir(root_path):
        PrettyMessaging.print_error('- parent-folder [{1}] does not exist'.format(root_path))
        raise(Exception('- parent-folder [{1}] does not exist'.format(root_path)))

    root_path = os.path.join(root_path, pname_sp)
    if os.path.isdir(root_path):
        msg = 'Project already exists'
        PrettyMessaging.print_error(msg)
        raise(Exception(msg))

    # Create directory
    os.makedirs(root_path)

    # One deeper to setup and configuration files
    root_path = os.path.join(root_path, pname_sp)
    os.makedirs(root_path)

    PrettyMessaging.print_info('- Root path: [{0}]'.format(root_path))

    # Create packages
    create_packages(pymakeconfigure, root_path)

    # Create resource folders
    create_resources(pymakeconfigure, root_path)

    # Generate default files
    create_default_files(pymakeconfigure, root_path)

    # Configure pymake
    configure_pymake(pymakeconfigure, root_path)

