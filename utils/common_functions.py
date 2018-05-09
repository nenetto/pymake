import json
import re
import copy
import pkg_resources
from inspect import getmembers, isfunction
from pymake.utils.prettymessaging import PrettyMessaging


def json2dict(path):
    with open(path, 'r') as fp:
        loaded_dict = json.load(fp)

    return loaded_dict


def get_pymake_var(var):
    pymakefile = pkg_resources.resource_filename('pymake', 'pymakefile.json')
    pymakevars = json2dict(pymakefile)

    if 'project-name' in pymakevars.keys():
        pm = PrettyMessaging()
    else:
        pm = PrettyMessaging('pymake')
        pm.print_error('Unknown var [{0}]'.format('project-name'))
        pm.print_error('Pymakefile during error:')
        pm.print_dict(pymakevars)
        exit(1)

    if var in pymakevars.keys():
        return pymakevars[var]
    else:
        pm.print_error('Unknown var [{0}]'.format(var))
        pm.print_error('Pymakefile during error:')
        pm.print_dict(pymakevars)
        exit(1)


def merge_dicts(a, b, path=None, replacement=True):
    """merges b into a"""
    pm = PrettyMessaging()
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            elif a[key] != b[key]:
                if replacement:
                    msg = 'Update [{1}] -> [{2}]'.format(key, a[key], b[key])
                    pm.print_warning(msg)
                    a[key] = b[key]  # Child step over
                else:
                    msg = 'Not updated [{1}] -/> [{2}]'.format(key, a[key], b[key])
                    pm.print_warning(msg)
                    pass
        else:
            a[key] = b[key]
    return a


def replace_vars(text, replacement_dict={}):
    replaced_text = copy.deepcopy(text)
    for old, new in replacement_dict.items():
        replaced_text = replaced_text.replace(str(old), str(new))
    return replaced_text


def replace(rule, configuration):
    replacement = {}
    var_value = None
    pm = PrettyMessaging()

    # Find pieces to replace in string type "{var-value}"
    for match in re.finditer('{[a-z]+(-*[a-z]*)*}', rule):
        var = match.group(0)

        var_name = var[1:-1]

        if var_name not in configuration.keys():
            pm.print_error('Unknown rule for [{0}]'.format(var))
            pm.print_error('Configuration during error:')
            pm.print_dict(configuration)
            exit(1)
        else:
            var_value = configuration[var_name]

        replacement[var] = var_value

    # Replace
    replaced_rule = copy.deepcopy(rule)
    for old, new in replacement.items():
        replaced_rule = replaced_rule.replace(str(old), str(new))
    return replaced_rule


def applymodifier(var_value, modifiers=[]):
    pm = PrettyMessaging()

    import pymake.utils.text_modifiers as tm
    allowed_modifiers_names = [f[0] for f in getmembers(tm) if isfunction(f[1])]

    if not isinstance(modifiers, list):
        modifiers = [modifiers]
        for m in modifiers:

            import pymake.utils.text_modifiers as tm

            if m not in allowed_modifiers_names:
                pm.print_warning('Unknown modifier [{0}] - Unchanged'.format(m))
            else:
                modifier_func = [f[1] for f in getmembers(tm) if f[0] == m][0]
                var_value = modifier_func(var_value)

    return var_value

