"""
ferrovial_servicios_a_bordo
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 12-05-2018
"""

from pymake.utils.common.prettymessaging import PrettyMessaging
from pymake.utils.common.scripting import run_commands
import sys
import pkg_resources
import subprocess


class FortiClient:

    def __init__(self, server, port, user, pwd):

        self._server = server
        self._port = port
        self._user = user
        self._pwd = pwd

        self._process = None

        self.pm = PrettyMessaging('Forticlient VPN')

    def connect(self):
        self.pm.print_info('Connecting to {0}'.format(self._server))
        cmd = 'connect_vpn {0}:{1} {2} {3}'.format(self._server,
                                                   self._port,
                                                   self._user,
                                                   self._pwd)

        self._process = subprocess.Popen(cmd, shell=True)
        self.pm.print_info('Connected')

    def disconnect(self):
        if self._process is not None:
            self._process.terminate()
            self._process.wait()
            self.pm.print_info('Disconnected')

    @staticmethod
    def install():

        # Check platform
        if sys.platform.startswith('linux'):
            script = pkg_resources.resource_filename('pymake',
                                                     'utils/vpn/forticlient/forticlient_docker_install_debian8.sh')

            cmd = '/bin/bash ' + script

            run_commands([cmd])

