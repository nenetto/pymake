"""
pycharm
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 09-05-2018
"""

import sys
from pymake.tools.create_setup import create_setup


def main(args=None):
    """Example of entry point"""
    if args is None:
        args = sys.argv[1:]

    print('This is the main function of pycharm')

    """Read the args"""
    if len(args) > 0:
        for i in args:
            print(i)

        if args[0] == 'create_setup':
            create_setup(args[1])
    else:
        print('No parameters passed')


if __name__ == "__main__":
    print('Welcome to the project [pycharm] created by [nenetto@gmail.com]')
    main()
