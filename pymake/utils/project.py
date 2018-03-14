import pkg_resources
import os
import json
import shutil
from pymake.utils import pymakeutils


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
    packages = get_value_pymakeconfigure(pymakeconfigure, 'packages', mandatory=False)
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


def get_value_pymakeconfigure(pymakeconfigure, var_name, mandatory=True):
    # Read pmake
    pmake_json = json.load(open(pymakeconfigure))

    if 'configuration' not in pmake_json.keys():
        msg = '\'configuration\' is not in pymake configure file'
        raise (ValueError(msg))
    else:
        pmake_json = pmake_json['configuration']

    # Check if var_name is in pmake file
    lost = var_name not in pmake_json.keys()

    # Check for mandatory
    if mandatory and lost:
        msg = 'Variable {var} is mandatory. Check your configuration'.format(var=var_name)
        raise(ValueError(msg))
    else:
        if lost:
            return None
        else:
            return pmake_json[var_name]


def create_packages(pymakeconfigure, root_path):
    # Extract name of project
    pname = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=False)
    print('[{0}] Creating packages'.format(pname))

    # Read package __init__.py template file
    project_init = pkg_resources.resource_filename('pymake', 'templates/python_package/__init__.template')
    project_init = pymakeutils.replace_template(project_init, pymakeconfigure)

    packages = get_value_pymakeconfigure(pymakeconfigure, 'packages', mandatory=False)
    for pack, conf in packages.items():
        print('[{0}]   - [{1}]'.format(pname, pack))

        pack_path = os.path.join(root_path, pack)
        os.makedirs(pack_path)

        file_path = os.path.join(pack_path, '__init__.py')
        with open(file_path, 'w') as f:
            f.write(project_init)


def configure_pymake(pymakeconfigure, root_path):

    pname = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=False)

    # Create pymake dir
    print('[{0}] Configuring pymake'.format(pname))
    pymake_path = os.path.join(root_path, 'pymake')
    os.makedirs(pymake_path)

    # Create folder setup
    setup_path = os.path.join(pymake_path, 'setup')
    os.makedirs(setup_path)

    # Setup.py
    print('[{0}] Setup:'.format(pname))
    print('[{0}]    - setup.template'.format(pname))
    setup_file = pkg_resources.resource_filename('pymake', 'templates/pymake/setup/setup.template')
    setup_file = pymakeutils.replace_template(setup_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(setup_path, 'setup.py.template')

    with open(file_path, 'w') as f:
        f.write(setup_file)

    # create_setup.py
    print('[{0}]    - create_setup.py'.format(pname))
    create_setup_file = pkg_resources.resource_filename('pymake', 'templates/pymake/setup/create_setup.template')
    create_setup_file = pymakeutils.replace_template(create_setup_file, pymakeconfigure, mandatory=False)

    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()
    create_setup_file = create_setup_file.replace('{project_name_package}', pname_sp)

    file_path = os.path.join(setup_path, 'create_setup.py')

    with open(file_path, 'w') as f:
        f.write(create_setup_file)

    # Create folder docker
    print('[{0}] Docker:'.format(pname))
    docker_path = os.path.join(pymake_path, 'docker')
    os.makedirs(docker_path)

    # Dockerfile
    print('[{0}]    - Dockerfile'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake', 'templates/pymake/docker/Dockerfile.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'Dockerfile.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # run_container_local
    print('[{0}]    - run_container_local.sh'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake', 'templates/pymake/docker/run_container_local.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'run_container_local.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # create_image
    print('[{0}]    - create_image.sh'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake',
                                                      'templates/pymake/docker/create_image.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'create_image.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # aws_push
    print('[{0}]    - aws_push.sh'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake',
                                                      'templates/pymake/docker/aws_push.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'aws_push.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # .dockerignore
    print('[{0}]    - .dockerignore'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake',
                                                      'templates/pymake/docker/dockerignore.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'dockerignore.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # create_docker_image.py
    print('[{0}]    - create_docker_image.py'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake', 'templates/pymake/docker/create_docker_image.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()
    dockerfile_file = dockerfile_file.replace('{project_name_package}', pname_sp)

    file_path = os.path.join(docker_path, 'create_docker_image.py')

    with open(file_path, 'w') as f:
        f.write(dockerfile_file)


def create_resources(pymakeconfigure, root_path):
    # Extract name of project
    pname = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=False)
    print('[{0}] Creating resources'.format(pname))
    resources = get_value_pymakeconfigure(pymakeconfigure, 'resource-folders', mandatory=False)

    for resource in resources:
        print('[{0}]   - [{1}]'.format(pname, resource))

        pack_path = os.path.join(root_path, resource)
        os.makedirs(pack_path)


def create_default_files(pymakeconfigure, root_path):
    pname = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=False)
    print('[{0}] Configuring files'.format(pname))

    # pymakefile.json
    print('[{0}]    - pymakefile.json'.format(pname))
    create_pymakefile(pymakeconfigure, root_path)
    pymakefile = os.path.join(root_path, 'pymakefile.json')

    # pymake_vars.py
    print('[{0}]    - pymake_vars.py'.format(pname))
    create_pymake_vars(pymakefile, root_path)

    # README.md
    print('[{0}]    - README.md'.format(pname))
    create_readme(pymakeconfigure, root_path)

    # __init__.py
    print('[{0}]    - __init__.py'.format(pname))
    create_init(pymakeconfigure, root_path)

    # main.py
    print('[{0}]    - main.py'.format(pname))
    create_main(pymakeconfigure, root_path)

    # pymakeconfiguration.json
    shutil.copy(pymakeconfigure, os.path.join(os.path.dirname(root_path), 'pymakeconfigure.json'))


def create_project(pymakeconfigure):

    # Extract name of project
    pname = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=False)
    print('[{0}] Creating project'.format(pname))
    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()


    # Extract directory root
    root_path = os.path.join(get_value_pymakeconfigure(pymakeconfigure, 'parent-folder'))

    # Check if exists
    if not os.path.isdir(root_path):
        msg = '[{0}] - parent-folder [{1}] does not exist'.format(pname, root_path)
        raise(Exception(msg))

    root_path = os.path.join(root_path, pname_sp)
    if os.path.isdir(root_path):
        msg = '[{0}] - Project already exists'.format(pname)
        raise(Exception(msg))

    # Create directory
    os.makedirs(root_path)

    # One deeper to setup and configuration files
    root_path = os.path.join(root_path, pname_sp)
    os.makedirs(root_path)

    print('[{0}] - Root path: [{1}]'.format(pname, root_path))

    # Create packages
    create_packages(pymakeconfigure, root_path)

    # Create resource folders
    create_resources(pymakeconfigure, root_path)

    # Generate default files
    create_default_files(pymakeconfigure, root_path)

    # Configure pymake
    configure_pymake(pymakeconfigure, root_path)