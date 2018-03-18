import pkg_resources
import os
import shutil
from pymake.utils import pymakeutils


def create_main(pymakeconfigure, root_path):

    # Read package __init__.py template file
    project_init = pkg_resources.resource_filename('pymake', 'templates/R_project/main.template')
    project_init = pymakeutils.replace_template(project_init, pymakeconfigure, mandatory=False)

    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()

    project_init = project_init.replace('{project_root}', pname_sp)

    file_path = os.path.join(root_path, 'main.R')

    with open(file_path, 'w') as f:
        f.write(project_init)


def create_readme(pymakeconfigure, root_path):

    # Read README.md template file
    readme = pkg_resources.resource_filename('pymake', 'templates/R_project/README.template')
    readme = pymakeutils.replace_template(readme, pymakeconfigure)

    file_path = os.path.join(os.path.dirname(root_path), 'README.md')

    with open(file_path, 'w') as f:
        f.write(readme)


def create_pymake_vars(pymakefile, root_path):

    # Read package vars.py template file
    project_vars = pkg_resources.resource_filename('pymake', 'templates/R_project/pymake_vars.template')
    project_vars = pymakeutils.replace_template(project_vars, pymakefile)

    file_path = os.path.join(root_path, 'project_vars.R')

    with open(file_path, 'w') as f:
        f.write(project_vars)


def create_pymakefile(pymakeconfigure, root_path):

    # Read package vars.py template file
    project_vars = pkg_resources.resource_filename('pymake', 'templates/R_project/pymakefile.template')
    project_vars = pymakeutils.replace_template(project_vars, pymakeconfigure)

    file_path = os.path.join(root_path, 'pymakefile.json')

    with open(file_path, 'w') as f:
        f.write(project_vars)


def create_rstudio_project(pymakeconfigure, root_path):
    # Read package vars.py template file
    project_vars = pkg_resources.resource_filename('pymake', 'templates/R_project/RProject.template')
    project_vars = pymakeutils.replace_template(project_vars, pymakeconfigure)

    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()

    file_path = os.path.join(root_path, '{0}.Rproj'.format(pname_sp))

    with open(file_path, 'w') as f:
        f.write(project_vars)

    # Add gitignore
    # Read package vars.py template file
    project_vars = pkg_resources.resource_filename('pymake', 'templates/R_project/gitignore.template')
    project_vars = pymakeutils.replace_template(project_vars, pymakeconfigure)

    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()

    file_path = os.path.join(root_path, '.gitignore')

    with open(file_path, 'w') as f:
        f.write(project_vars)


def create_default_files(pymakeconfigure, root_path):
    pname = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=False)
    print('[{0}] Configuring files'.format(pname))

    # pymakefile.json
    print('[{0}]    - pymakefile.json'.format(pname))
    create_pymakefile(pymakeconfigure, root_path)
    pymakefile = os.path.join(root_path, 'pymakefile.json')

    # pymake_vars.py
    print('[{0}]    - pymake_vars.R'.format(pname))
    create_pymake_vars(pymakefile, root_path)

    # README.md
    print('[{0}]    - README.md'.format(pname))
    create_readme(pymakeconfigure, root_path)

    # main.py
    print('[{0}]    - main.R'.format(pname))
    create_main(pymakeconfigure, root_path)

    # pymakeconfiguration.json
    shutil.copy(pymakeconfigure, os.path.join(os.path.dirname(root_path), 'pymakeconfigure.json'))

    # RStudio Project configuration
    print('[{0}]    - RStudio Project configuration'.format(pname))
    create_rstudio_project(pymakefile, root_path)


def create_resources(pymakeconfigure, root_path):
    # Extract name of project
    pname = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=False)
    print('[{0}] Creating resources'.format(pname))
    resources = pymakeutils.get_value_pymakeconfigure(pymakeconfigure, 'resource-folders', mandatory=False)

    for resource in resources:
        print('[{0}]   - [{1}]'.format(pname, resource))

        pack_path = os.path.join(root_path, resource)
        os.makedirs(pack_path)


def configure_pymake(pymakeconfigure, root_path):

    pname = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=False)

    # Create pymake dir
    print('[{0}] Configuring pymake'.format(pname))
    pymake_path = os.path.join(root_path, 'pymake')
    os.makedirs(pymake_path)

    # Create folder setup
    # TODO: https://hilaryparker.com/2014/04/29/writing-an-r-package-from-scratch/

    # Create folder docker
    print('[{0}] Docker:'.format(pname))
    docker_path = os.path.join(pymake_path, 'docker')
    os.makedirs(docker_path)

    # Dockerfile
    print('[{0}]    - Dockerfile'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake', 'templates/pymake/docker_R/Dockerfile.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'Dockerfile.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # create_image
    print('[{0}]    - create_image.sh'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake',
                                                      'templates/pymake/docker_R/create_image.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'create_image.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # run_container_local
    print('[{0}]    - run_container_local.sh'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake',
                                                      'templates/pymake/docker_R/run_container_local.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'run_container_local.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # aws_push
    print('[{0}]    - aws_push.sh'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake',
                                                      'templates/pymake/docker_R/aws_push.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'aws_push.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # .dockerignore
    print('[{0}]    - .dockerignore'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake',
                                                      'templates/pymake/docker_R/dockerignore.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'dockerignore.template')
    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # install_package_command
    print('[{0}]    - install_package_command'.format(pname))
    install_package_command_file = pkg_resources.resource_filename('pymake',
                                                      'templates/pymake/docker_R/install_package_command.template')
    install_package_command_file = pymakeutils.replace_template(install_package_command_file, pymakeconfigure, mandatory=False)

    file_path = os.path.join(docker_path, 'install_package_command.template')
    with open(file_path, 'w') as f:
        f.write(install_package_command_file)

    # install_package_command
    print('[{0}]    - install_R_dependencies'.format(pname))
    install_R_dependencies_file = pkg_resources.resource_filename('pymake',
                                                                   'templates/pymake/docker_R/install_R_dependencies.template')
    install_R_dependencies_file = pymakeutils.replace_template(install_R_dependencies_file, pymakeconfigure,
                                                                mandatory=False)

    file_path = os.path.join(docker_path, 'install_R_dependencies.template')
    with open(file_path, 'w') as f:
        f.write(install_R_dependencies_file)

    # create_docker_image.py
    print('[{0}]    - create_docker_image.py'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake', 'templates/pymake/docker_R/create_docker_image.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()
    dockerfile_file = dockerfile_file.replace('{project_name_package}', pname_sp)

    file_path = os.path.join(docker_path, 'create_docker_image.py')

    with open(file_path, 'w') as f:
        f.write(dockerfile_file)

    # main.sh
    print('[{0}]    - main.sh'.format(pname))
    dockerfile_file = pkg_resources.resource_filename('pymake',
                                                      'templates/pymake/docker_R/main.template')
    dockerfile_file = pymakeutils.replace_template(dockerfile_file, pymakeconfigure, mandatory=False)

    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()
    dockerfile_file = dockerfile_file.replace('{project_root}', pname_sp)

    file_path = os.path.join(docker_path, 'main.template')

    with open(file_path, 'w') as f:
        f.write(dockerfile_file)


def create_project(pymakeconfigure):
    # Extract name of project
    pname = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=False)
    pname_sp = pymakeutils.get_value_pymakefile(pymakeconfigure, 'project_name', convert_spaces=True).lower()

    # Extract directory root
    root_path = os.path.join(pymakeutils.get_value_pymakeconfigure(pymakeconfigure, 'parent-folder'))

    # Check if exists
    if not os.path.isdir(root_path):
        msg = '[{0}] - parent-folder [{1}] does not exist'.format(pname, root_path)
        raise (Exception(msg))

    root_path = os.path.join(root_path, pname_sp)
    if os.path.isdir(root_path):
        msg = '[{0}] - Project already exists'.format(pname)
        raise (Exception(msg))

    # Create directory
    os.makedirs(root_path)

    # One deeper to setup and configuration files
    root_path = os.path.join(root_path, pname_sp)
    os.makedirs(root_path)

    print('[{0}] - Root path: [{1}]'.format(pname, root_path))

    create_default_files(pymakeconfigure, root_path)

    create_resources(pymakeconfigure, root_path)

    configure_pymake(pymakeconfigure, root_path)
