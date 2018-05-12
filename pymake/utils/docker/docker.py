"""
ferrovial_servicios_a_bordo
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 12-05-2018
"""
import os


def iscontainer():

    if os.path.isfile('/.dockerenv'):
        return True
    else:
        return False
