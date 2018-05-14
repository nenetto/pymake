"""
pycharm
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 09-05-2018
"""

from pymake.utils.common.prettymessaging import PrettyMessaging
printer = PrettyMessaging('pymake')
import sys

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
            remove = False
            if len(args) > 2:
                if args[2] == '-removeold':
                    remove = True

            from pymake.tools.create_setup import create_setup
            create_setup(args[1], remove)
    else:
        print('No parameters passed')


if __name__ == "__main__":
    print('Welcome to the project [pycharm] created by [nenetto@gmail.com]')
    main()
