# Standard library
import os
import subprocess
# Overlord library
from web.settings import BASE_DIR, LOGGER_DIR
from core.library.time import timestamp


class Console:
  # Colour Pallet
  colours = {
    "red": '\33[31m',
    "green": '\33[32m',
    "yellow": '\33[33m',
    "blue": '\33[34m',
    "white": '\33[0m',
    "flash": '\33[5;30m',
    "error": '\33[1;31m',
    "success": '\33[1;32m'
  }
  wait = "\33[5;33m🔶\33[0m"

  def __init__(self, cmd=None, *args, **kwargs) -> None:
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

  def out(self, text="", colour:str = "white", print_to_console:bool = True, end:str = '\n') -> str:
    """
    Returns a string converted variable [text] wrapped in colour
    tags to the console which also end by defaulting back to
    the selected default colour option [self.default_col]

    :param text any: stringified variable for colour context
    :param colour str: name of colour 'key' from colour pallet [self.out]
    :return str: string wrapped in colour tags ie; "\33[31m Example \33[0m"
    """

    def p(t):
      t = t + self.default_col
      if print_to_console:
        print(t, end=end)
      return t

    text = str(text)
    if colour in self.colours:
      return p(self.colours[colour] + text)
    elif colour is None:
      return p(self.default_col + text)

    return p(
      self.colours["red"] + \
      f"[ Console Error: No such colour option `{colour}` ]" + \
      self.colours["yellow"] + text
    )

  def status(self, status:str, message:str = None) -> str:
    """
    Using the type of the status to determine the input (int == http status code // str == api response)
    returns a string with the appropriate colour for the status code.

    :param status any: HTTP status code (int) or API response (str)
    :return str:
    """
    txt = status if message is None else message

    # HTTP Status Code Colours
    if isinstance(status, int):
      if 100 <= status <= 199:
        return self.out(' [UNKNOWN] ' + txt, 'white')
      elif 200 <= status <= 299:
        return self.out(' [SUCCESS] ' + txt, 'green')
      elif 300 <= status <= 399:
        return self.out(' [WARNING] ' + txt, 'yellow')
      else:
        return self.out(' [ERROR] ' + txt, 'red')

    # API Response Colours
    elif isinstance(status, str):
      if status == 'BAD':
        return self.out(' [ERROR] ' + txt, 'red')
      elif status == 'OK':
        return self.out(' [SUCCESS] ' + txt, 'green')
      else:
        return self.out(' [WARNING] ' + txt, 'yellow')

  def input(self, command:str, cwd:str = BASE_DIR, show_output:bool = False) -> str:
    """
    Using the os.system() method execute the command (a string) in a sub-shell.
    This method is implemented by calling the standard C function system(), and has the same limitations.

    :param command str: the input command(s) to send to the system
    :return str: the returncode if output was shown or the output if it was not shown
    """
    if show_output:
      out = subprocess.call(
        command,
        shell=True,
        cwd=cwd
      )
      return out.returncode
    else:
      out = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        encoding='utf-8'
      )
      return out.stdout

  def run_script(self, path:str) -> object:
    """
    Using the console.input method; run a script from the tools/scripts directory.

    :param path str: path to the script from within "tools/scripts"
    :return None:
    """
    return subprocess.call(['sh', f'{BASE_DIR}/tools/scripts/{path}.sh'])

  @staticmethod
  def log(_input, print_to_console:bool = False) -> None:
    """
    Writes output to the logger file and then also prints it into the console

    :param input any: converts what ever is given into a string to be logged
    :return None:
    """
    if print_to_console:
      print(_input)

    _input = _input.replace('\n', '\n                      ')
    _input = f'\n[{timestamp()}] {_input}'

    if os.path.exists(LOGGER_DIR):
      content = ''
      with open(LOGGER_DIR, 'r') as logger:
        content = logger.read()
      with open(LOGGER_DIR, 'w+') as logger:
        logger.write(content + _input)


console = Console()
