# Standard library
import subprocess
from os import system as _system
# Overlord library
from web.settings import BASE_DIR


def col(text, colour):
    text = str(text)
    if colour == 'red': r = '\33[31m' + text
    elif colour == 'green': r = '\33[32m' + text
    elif colour == 'yellow': r = '\33[33m' + text
    elif colour == 'blue': r = '\33[34m' + text
    elif colour == 'purple': r = '\33[35m' + text
    elif colour == 'lg': r = '\33[36m' + text
    else: r = '\33[0m' + text
    return r + '\33[0m'


def colour_status_code(status):
    if isinstance(status, int):
        if 100 <= status <= 199: return col(status, 'white')
        elif 200 <= status <= 299: return col(status, 'green')
        elif 300 <= status <= 399: return col(status, 'yellow')
        else: return col(status, 'red')
    elif isinstance(status, str):
        if status == 'BAD': return col(status, 'red')
        elif status == 'OK': return col(status, 'green')
        else: return col(status, 'yellow')


class Console:
    # ===== Colour Pallet ======
    palette = {
        "red": '\33[31m',
        "green": '\33[32m',
        "yellow": '\33[33m',
        "white": '\33[0m',
    }

    def __init__(self, *args, **kwargs):
        # Style Settings
        self.default_col = self.col["white"]

    def col(self, text="", colour=None):
        """
        Returns a string converted variable [text] wrapped in colour
        tags to the console which also end by defaulting back to
        the selected default colour option [self.default_col]

        :param text any: stringified variable for colour context
        :param colour str: name of colour 'key' from colour pallet [self.col]
        :return: string wrapped in colour tags ie; "\33[31m Example \33[0m"
        """
        # Always use string method & and use default colour when not defined
        text = str(text)
        choice = colour if not colour is None else self.default_col

        # Select colour and return
        for name, code in self.palette:
            if name == choice:
                return print(code + text + self.default_col)

        # Return stylized error
        return print(self.col["red"] + \
            f"[Console Error: No such colour option `{colour}` ]" + \
            self.col["yellow"] + text + self.default_colour)

    def http_status(status):
        """
        Using the type of the status to determine the input (int == http status code // str == api response)
        returns a string with the appropriate colour for the status code.

        :param status any: HTTP status code (int) or API response (str)
        :return str:
        """
        if isinstance(status, int):
            if 100 <= status <= 199:
                return print(col(status, 'white'))
            elif 200 <= status <= 299:
                return print(col(status, 'green'))
            elif 300 <= status <= 399:
                return col(status, 'yellow')
            else:
                return col(status, 'red')
        elif isinstance(status, str):
            if status == 'BAD':
                return col(status, 'red')
            elif status == 'OK':
                return col(status, 'green')
            else:
                return col(status, 'yellow')

    def input(self, command):
        """
        Using the os.system() method execute the command (a string) in a sub-shell. This method is implemented by calling
        the standard C function system(), and has the same limitations.

        :param command str: the input command(s) to send to the system
        :return None:
        """
        return _system(command)

    def run_script(self, path, arguments=None):
        """
        Using the console.input method; run a script from the tools/scripts directory.

        :param path str: path to the script from within "tools/scripts"
        :return: script output
        """
        if arguments is None:
            arguments = []
        return subprocess.run(
            [f"{BASE_DIR}/tools/scripts/{path}.sh", ] + arguments,
            bufsize=1,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            universal_newlines=True
        )
