import json
from pprint import pformat
import pkg_resources
import re


def get_value_pymakefile(pymakefile,
                         var_name,
                         mandatory=False,
                         convert_spaces=False,
                         default=''):

    # Read pmake
    pmake_json = json.load(open(pymakefile))

    var_name = var_name.replace('_', '-')

    # Check if var_name is in pmake file
    lost = var_name not in pmake_json.keys()

    # Check for header
    if lost:
        if var_name == 'header':
            return get_header(pymakefile)
        if var_name == 'pymakefile-vars':
            return get_pymakevars(pymakefile)


    # Check for mandatory
    if mandatory and lost:
        msg = 'Variable {var} is mandatory. Check your pymakefile.pmake'.format(var=var_name)
        raise(ValueError(msg))
    else:
        # Replace by default value
        if lost:
            var_value = default
        else:
            var_value = pmake_json[var_name]

        # Replace spaces
        if convert_spaces:
            var_value = var_value.replace(' ', '_')

    return str(var_value)


def replace_template(templatefile, pymakefile, mandatory=True):

    with open(templatefile, 'r') as tf:
        tf_str = tf.read()

    for match in re.finditer('{[a-z]+(_*[a-z]*)*}', tf_str):
        var_name = match.group(0)
        var_name_hyp = var_name[1:-1]
        var_value = get_value_pymakefile(pymakefile, var_name_hyp, mandatory=mandatory, convert_spaces=False)

        #print('Replacing [{0}] by [{1}]'.format(var_name[1:-1], var_value))
        if mandatory:
            tf_str = tf_str.replace(var_name, var_value)
        elif var_value != '':
            tf_str = tf_str.replace(var_name, var_value)

    return tf_str


def get_header(pymakefile):
    # Read header template file
    header = pkg_resources.resource_filename('pymake', 'templates/python_project/header.template')
    header = replace_template(header, pymakefile)

    return header


def get_pymakevars(pymakefile):
    # Read pmake
    pmake_json = json.load(open(pymakefile))
    str_pmake_json = pformat(pmake_json)
    return str_pmake_json[1:-1]

