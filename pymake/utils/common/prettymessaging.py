"""
pycharm
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 09-05-2018
"""

from tabulate import tabulate
from pprint import pprint
import sys
import json


class PrettyMessaging:

    color_codes = {
        # Reset
        'Color_Off': '\033[0m',      # Text Reset

        # Regular Colors
        'Black': '\033[0;30m',        # Black
        'Red': '\033[0;31m',          # Red
        'Green': '\033[0;32m',        # Green
        'Yellow': '\033[0;33m',       # Yellow
        'Blue': '\033[0;34m',         # Blue
        'Purple': '\033[0;35m',       # Purple
        'Cyan': '\033[0;36m',         # Cyan
        'White': '\033[0;37m',        # White

        # Bold
        'BBlack': '\033[1;30m',       # Black
        'BRed': '\033[1;31m',         # Red
        'BGreen': '\033[1;32m',       # Green
        'BYellow': '\033[1;33m',      # Yellow
        'BBlue': '\033[1;34m',        # Blue
        'BPurple': '\033[1;35m',      # Purple
        'BCyan': '\033[1;36m',        # Cyan
        'BWhite': '\033[1;37m',       # White

        # Underline
        'UBlack': '\033[4;30m',       # Black
        'URed': '\033[4;31m',         # Red
        'UGreen': '\033[4;32m',       # Green
        'UYellow': '\033[4;33m',      # Yellow
        'UBlue': '\033[4;34m',        # Blue
        'UPurple': '\033[4;35m',      # Purple
        'UCyan': '\033[4;36m',        # Cyan
        'UWhite': '\033[4;37m',       # White

        # Background
        'On_Black': '\033[40m',       # Black
        'On_Red': '\033[41m',         # Red
        'On_Green': '\033[42m',       # Green
        'On_Yellow': '\033[43m',      # Yellow
        'On_Blue': '\033[44m',        # Blue
        'On_Purple': '\033[45m',      # Purple
        'On_Cyan': '\033[46m',        # Cyan
        'On_White': '\033[47m',       # White

        # High Intensity
        'IBlack': '\033[0;90m',       # Black
        'IRed': '\033[0;91m',         # Red
        'IGreen': '\033[0;92m',       # Green
        'IYellow': '\033[0;93m',      # Yellow
        'IBlue': '\033[0;94m',        # Blue
        'IPurple': '\033[0;95m',      # Purple
        'ICyan': '\033[0;96m',        # Cyan
        'IWhite': '\033[0;97m',       # White

        # Bold High Intensity
        'BIBlack': '\033[1;90m',      # Black
        'BIRed': '\033[1;91m',        # Red
        'BIGreen': '\033[1;92m',      # Green
        'BIYellow': '\033[1;93m',     # Yellow
        'BIBlue': '\033[1;94m',       # Blue
        'BIPurple': '\033[1;95m',     # Purple
        'BICyan': '\033[1;96m',       # Cyan
        'BIWhite': '\033[1;97m',      # White

        # High Intensity backgrounds
        'On_IBlack': '\033[0;100m',   # Black
        'On_IRed': '\033[0;101m',     # Red
        'On_IGreen': '\033[0;102m',   # Green
        'On_IYellow': '\033[0;103m',  # Yellow
        'On_IBlue': '\033[0;104m',    # Blue
        'On_IPurple': '\033[0;105m',  # Purple
        'On_ICyan': '\033[0;106m',    # Cyan
        'On_IWhite': '\033[0;107m',   # White
    }

    print_colors = {
        '1': color_codes['BIGreen'],
        '2': color_codes['Yellow'],
        '3': color_codes['BIBlue'],
        'warningH': color_codes['On_Green'] + color_codes['BBlack'],
        'warning': color_codes['Green'],
        'errorH': color_codes['On_Red'] + color_codes['BBlack'],
        'error': color_codes['Red'],
        'off': color_codes['Color_Off']
    }

    def __init__(self, header_text=None):
        if header_text is not None:
            self._header = str(header_text)
        else:
            self._header = 'pymake'

        self.percentage_called = False

    @property
    def header(self):
        return self._header

    def project_header(self, padding):
        header = self.print_colors['1'] + '[' + self.header + ']' + self.print_colors['off']
        separator = self.print_colors['1'] + ': ' + self.print_colors['off'] + '  ' * padding
        return header, separator

    def print_info(self, msg, padding=0):
        header, separator = self.project_header(padding)
        header_info = header + self.print_colors['1'] + '[   info]' + self.print_colors['off'] + separator
        msg = header_info + self.print_colors['2'] + msg + self.print_colors['off']

        if self.percentage_called:
            msg = '\n' + msg

        print(msg)

    def print_info_2(self, msg, padding=0):
        header, separator = self.project_header(padding)
        header_info = header + self.print_colors['1'] + '[   info]' + self.print_colors[
            'off'] + separator
        msg = header_info + self.print_colors['3'] + msg + self.print_colors['off']
        if self.percentage_called:
            msg = '\n' + msg
        print(msg)

    def print_error(self, msg, exit_code=None, raise_error=None, padding=0):
        header, separator = self.project_header(padding)
        header_info = header + self.print_colors['errorH'] + '[#error#]' + self.print_colors[
            'off'] + separator
        msg = header_info + self.print_colors['error'] + msg + self.print_colors['off']
        if self.percentage_called:
            msg = '\n' + msg
        print(msg)

        if raise_error is not None:
            raise raise_error

        if exit_code is not None:
            exit(exit_code)

    def print_warning(self, msg, padding=0):
        header, separator = self.project_header(padding)
        header_info = header + self.print_colors['warningH'] + '[warning]' + self.print_colors['off'] + separator
        msg = header_info + self.print_colors['warning'] + msg + self.print_colors['off']
        if self.percentage_called:
            msg = '\n' + msg
        print(msg)

    def print_separator(self, size=67):
        msg = self.print_colors['2'] + '-'*size + self.print_colors['off']
        if self.percentage_called:
            msg = '\n' + msg
        print(msg)

    def print_json(self, path):
        with open(path, 'r') as fp:
            example_conf = json.load(fp)

            self.print_separator()
        print(self.print_colors['2'])
        pprint(example_conf)
        print(self.print_colors['off'])
        self.print_separator()

    def print_dict(self, input_dict):
        self.print_separator()
        print(self.print_colors['2'])
        pprint(input_dict)
        print(self.print_colors['off'])
        self.print_separator()

    def print_pandas_df(self, df, n=5):
        if n is None:
            n = df.shape[0]

        print(self.print_colors['2'])
        print(tabulate(df.head(n), headers='keys', tablefmt='psql'))
        print(self.print_colors['off'])

    def print_info_percentage(self, percentage, msg_pre='', msg_post='', padding=0):
        self.percentage_called = True

        header, separator = self.project_header(padding)
        header_info = header + self.print_colors['1'] + '[   info]' + self.print_colors['off'] + separator

        msg = header_info
        msg += self.print_colors['2']
        msg += msg_pre
        msg += self.print_colors['off']
        msg += self.print_colors['3']
        msg += ': [ {0:.2f} %]-'.format(percentage)
        msg += self.print_colors['2'] + msg_post
        msg += self.print_colors['off']

        if percentage >= 100:
            str1 = "\r{0}\n".format(msg)
            self.percentage_called = False
        else:
            str1 = "\r{0}".format(msg)

        sys.stdout.write(str1)
        sys.stdout.flush()

    def print_info_flush(self, msg='', wait=True, padding=0):
        self.percentage_called = True

        header, separator = self.project_header(padding)
        header_info = header + self.print_colors['1'] + '[   info]' + self.print_colors['off'] + separator

        msgc = header_info
        msgc += self.print_colors['2']
        msgc += msg
        msgc += self.print_colors['off']

        if wait:
            str1 = "\r{0}".format(msgc)
        else:
            str1 = "\r{0}\n".format(msgc)
            self.percentage_called = False

        sys.stdout.write(str1)
        sys.stdout.flush()