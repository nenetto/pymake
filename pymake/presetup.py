"""
ferrovial_servicios_a_bordo
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 12-05-2018
"""

from pymake.utils.sql.mssql import MsSQL
from pymake.utils.vpn.forticlient import FortiClient


# Install packages

def preinstall():

    MsSQL.install()

    FortiClient.install()
