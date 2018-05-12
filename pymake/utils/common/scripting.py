"""
ferrovial_servicios_a_bordo
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 12-05-2018
"""
import pexpect
import subprocess
from pymake.utils.common.prettymessaging import PrettyMessaging
import sys


def run_commands(commands_list):

    pm = PrettyMessaging('pymake')

    n = len(commands_list)
    i = 0
    for c in commands_list:
        result = subprocess.check_output(c.split(' ')).decode("utf-8")[:-1]
        i += 1
        pm.print_info_percentage(100 * i / n, 'Running', str(c))

        pm.print_separator()
        print(result)
        pm.print_separator()


def run_commands_expect(commands_dict):

    pm = PrettyMessaging('pymake')

    n = len(commands_dict)
    i = 0
    for cname, v in commands_dict.items():
        pm.print_info_percentage(100 * i / n, 'Running', cname)

        cmd = v['command']
        str_expect = v['expect'] if 'expect' in v else None
        str_response = v['response'] if 'response' in v else None

        if str_expect:
            child = pexpect.spawn('/bin/bash', ['-c', cmd], timeout=120, encoding='utf-8')  # the command you want to run
            child.expect(str_expect)  # the string you expect
            child.sendline(str_response)  # the string with which you'd like to respond
            child.wait()  # wait for the child to exit
        else:
            subprocess.check_call(cmd)

        i += 1
        pm.print_info_percentage(100 * i / n, 'Running', cname)


def run_expect_command(command, str_expect=None, str_response=''):

    if str_expect:
        child = pexpect.spawn(command)  # the command you want to run
        child.expect(str_expect)  # the string you expect
        child.sendline(str_response)  # the string with which you'd like to respond
        child.wait()  # wait for the child to exit
    else:
        result = subprocess.check_output(command.split(' ')).decode("utf-8")[:-1]
