"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 12-05-2018
"""
import subprocess
from pymake.main import printer as pm


def run_shell_command(command):

    session = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = session.communicate()
    session.wait()

    output_lines = stdout.decode("utf-8").split('\n')
    for ol in output_lines:
        pm.print_info_2(ol, padding=3)

    if session.returncode != 0:
        e = stderr.decode("utf-8")
        pm.print_error('Installation failed!')
        pm.print_info_2('Error: {0}'.format(str(e)))
        pm.print_error('Exit', exit_code=0)

    else:
        e = stderr.decode("utf-8").split('\n')
        for ee in e:
            pm.print_info(ee, padding=4)