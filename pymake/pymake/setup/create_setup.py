"""
pymake
-------------------------------

pymake package

 - E. Marinetto
 - nenetto@gmail.com
"""
import os
import sys
import subprocess
import glob
from pprint import pformat
import pipreqs
import pkg_resources
from pymake.project_vars import project_vars, PrettyMessaging

PrettyMessaging.print_separator()
PrettyMessaging.print_info('Configuring setup for project')

# Read pymake folder
PrettyMessaging.print_info('Reading pymake folder')
pymake_path = os.path.abspath(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), os.pardir))

# main package folder
package_path = os.path.abspath(os.path.join(pymake_path, os.pardir))

# Configuring Package data
PrettyMessaging.print_info('Looking for resources')
root_path = os.path.abspath(os.path.join(os.path.pardir, os.path.pardir))


package_data_list = []


this_dir = os.path.dirname(os.path.realpath(__file__))
for root, directories, filenames in os.walk(root_path):
    for filename in filenames:
        if root != this_dir:
            abs_path = os.path.join(root, filename)
            common_prefix = os.path.commonprefix([package_path, abs_path])
            path2add = os.path.relpath(abs_path, common_prefix)

            if '__pycache__' not in path2add:
                package_data_list.append(path2add)
                PrettyMessaging.print_info('   - [{0}]'.format(os.path.split(path2add)[-1]))

package_data = {'': package_data_list}


# Configuring requirements data
# Create requirements file using pipreqs

FNULL = open(os.devnull, 'w')
PrettyMessaging.print_info('Looking for requirements')
subprocess.check_call(['pipreqs', '--force', '{0}'.format(root_path)], stdout=FNULL, stderr=FNULL)
requirements_file_path = os.path.join(root_path, 'requirements.txt')

requirements = []
with open(requirements_file_path, 'r') as f:
    content = f.readlines()

content = [x.strip().replace('==', '>=') for x in content]
if content != ['']:
    requirements = requirements + content

for r in requirements:
    PrettyMessaging.print_info('   - [{0}]'.format(r))

# Delete requirements file
os.remove(requirements_file_path)

# Configuring entry point
PrettyMessaging.print_info('Configuring entry point')
project_entry_point = project_vars['project-name'].replace(' ', '_').lower()
PrettyMessaging.print_info('   - [{0} => {0}.main:main]'.format(project_entry_point))


# Create setup.py
PrettyMessaging.print_info('Generating setup.py')
# If setup.py, delete old

project_path = os.path.abspath(os.path.join(package_path, os.pardir))

setup_file_path = os.path.join(project_path, 'setup.py')
if os.path.exists(setup_file_path) and os.path.isfile(setup_file_path):
    PrettyMessaging.print_info('Deleting old setup.py')
    os.remove(setup_file_path)

setup_template = pkg_resources.resource_filename(__name__, 'setup.py.template')

# Replacing variables
PrettyMessaging.print_info('Reading template setup.py')
with open(setup_template, 'r') as setup_file:
    setup_text = setup_file.read()

PrettyMessaging.print_info('Setting variables setup.py')
setup_text = setup_text.replace('{package_data}', pformat(package_data))
setup_text = setup_text.replace('{package_requirements}', str(requirements))
setup_text = setup_text.replace('{project_entry_point}', project_entry_point)

PrettyMessaging.print_info('Saving setup.py')

with open(setup_file_path, 'w') as setup_file:
    setup_file.write(setup_text)

PrettyMessaging.print_info('Setup.py created successfully')
PrettyMessaging.print_separator()