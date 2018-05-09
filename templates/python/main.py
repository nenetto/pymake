#parse('header.py')
import sys


def main(args=None):
    """Example of entry point"""
    if args is None:
        args = sys.argv[1:]

    print('This is the main function of ${PROJECT_NAME}')

    """Read the args"""
    if len(args) > 0:
        for i in args:
            print(i)

        first_arg = args[0]

        print('You passed the parameter [{0}]'.format(first_arg))

    else:
        print('No parameters passed')


if __name__ == "__main__":
    print('Welcome to the project [${PROJECT_NAME}] created by [${AUTHOR_EMAIL}]')
    main()
