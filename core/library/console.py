# Standard library
import os
import subprocess
from os import system as _system
# Overlord library
from web.settings import BASE_DIR, LOGGER_DIR
from core.library.time import timestamp


class Console:
  # Colour Pallet
  colours = {
    "red": '\33[31m',
    "green": '\33[32m',
    "yellow": '\33[33m',
    "white": '\33[0m',
  }

  def __init__(self, cmd=None, *args, **kwargs):
    """
    INITIALIZE OVERLORD CONSOLE
      - Set default colour
      - Run initial input (if any)
    """

    # Style Settings
    self.default_col = self.colours["white"]

    # Input options
    self.input(f"cd {BASE_DIR}")
    if cmd is not None:
      self.input(cmd)

  def output(self, text="", colour=None):
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

    # Select colour and return
    if colour in self.colours:
      return self.colours[colour] + text + self.default_col

    # Return stylized error
    return self.colours["red"] + \
      f"[ Console Error: No such colour option `{colour}` ]" + \
      self.colours["yellow"] + text + self.default_colour

  def status(self, status):
    """
    Using the type of the status to determine the input (int == http status code // str == api response)
    returns a string with the appropriate colour for the status code.

    :param status any: HTTP status code (int) or API response (str)
    :return str:
    """

    # HTTP Status Code Colours
    if isinstance(status, int):
      if 100 <= status <= 199:
        return self.col(status, 'white')
      elif 200 <= status <= 299:
        return self.col(status, 'green')
      elif 300 <= status <= 399:
        return self.col(status, 'yellow')
      else:
        return self.col(status, 'red')

    # API Response Colours
    elif isinstance(status, str):
      if status == 'BAD':
        return self.col(status, 'red')
      elif status == 'OK':
        return self.col(status, 'green')
      else:
        return self.col(status, 'yellow')

  def input(self, command):
    """
    Using the os.system() method execute the command (a string) in a sub-shell.
    This method is implemented by calling the standard C function system(), and has the same limitations.

    :param command str: the input command(s) to send to the system
    :return None:
    """
    return _system(command)

  def run_script(self, path):
    """
    Using the console.input method; run a script from the tools/scripts directory.

    :param path str: path to the script from within "tools/scripts"
    :return None:
    """
    return subprocess.call(['sh', f'{BASE_DIR}/tools/scripts/{path}.sh'])

  @staticmethod
  def log(_input):
    """
    Writes output to the logger file and then also prints it into the console

    :param input any: converts what ever is given into a string to be logged
    :return None:
    """
    _input = _input.replace('\n', '\n                      ')
    _input = f'\n[{timestamp()}] {_input}'

    if os.path.exists(LOGGER_DIR):
      content = ''
      with open(LOGGER_DIR, 'r') as logger:
        content = logger.read()
      with open(LOGGER_DIR, 'w+') as logger:
        logger.write(content + _input)
    else:
      con = Console()
      con.output(_input, "yellow")


console = Console()
