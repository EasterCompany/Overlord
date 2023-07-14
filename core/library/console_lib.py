# Standard library
import os
import subprocess
from getpass import getpass
# Overlord library
from core.library.time import timestamp
from web.settings import BASE_DIR, LOGGER_DIR

sudo_pass:str|None = None


def prompt_sudo_pass() -> str:
  global sudo_pass
  sudo_pass = getpass("  [sudo] enter password: ")
  print()
  return sudo_pass


def sudo(function):
  def sudo_required_function(*args, **kwargs):
    _sudo_pass = prompt_sudo_pass() if sudo_pass == None else sudo_pass
    return function(sudo_pass=_sudo_pass, *args, **kwargs)
  return sudo_required_function


class Console:
  # Color Pallet
  colours = {
    "red": '\33[31m',
    "green": '\33[32m',
    "yellow": '\33[33m',
    "orange": '\33[33m',
    "amber": '\33[33m',
    "blue": '\33[34m',
    "white": '\33[0m',
    "flash": '\33[5;30m',
    "error": '\33[1;31m',
    "success": '\33[1;32m'
  }
  wait = "\33[5;33m🔶\33[0m"
  success = "✅"
  failure = "❌"
  __log_cache__ = []

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

    # Clear log cache
    self.clear_log_cache()

  def clear_log_cache(self):
    ''' Clears the log cache '''
    self.__log_cache__ = []

  def append_log_cache(self, output):
    ''' Appends output to the log cache '''
    self.__log_cache__.append(output)

  def output(self, text="", colour:str = "white", print_to_console:bool = True, end:str = '\n') -> str:
    """ console.out alias function """
    return self.out(text, colour, print_to_console, end)

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
        self.append_log_cache([t, end])
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

  def status(self, status:str, message=None) -> str:
    """
    Using the type of the status to determine the input (int == http status code // str == api response)
    returns a string with the appropriate colour for the status code.

    :param status any: HTTP status code (int) or API response (str)
    :return str:
    """
    txt = status if message is None else str(message)

    # HTTP Status Code Colors
    if isinstance(status, int):
      if 100 <= status <= 199:
        return self.out(f'{txt}', 'white', False)
      elif 200 <= status <= 299:
        return self.out(f'{txt}', 'green', False)
      elif 300 <= status <= 399:
        return self.out(f'{txt}', 'yellow', False)
      else:
        return self.out(f'{txt}', 'red', False)

    # API Response Colors
    elif isinstance(status, str):
      status = status.lower()
      if status == 'bad' or status == 'error':
        return self.out(f'{txt}', 'red', False)
      elif status == 'ok':
        return self.out(f'{txt}', 'green', False)
      else:
        return self.out(f'{txt}', 'yellow', False)

  def verify(self, warning:str|None = None, message:str|None = None):
    """
    Prints a message asking for the user to verify using the options (Y/N) whether not
    the user wishes to proceed with the current action.

    :return bool: true if the user verifies, false if not
    """
    print()

    if message is None:
      message = "  Do you still wish to proceed? (Y/N): "
    if warning is not None:
      console.out(warning, "amber")

    response = input(message)
    print()
    return True if response.lower() == 'y' or response.lower() == 'yes' else False

  def input(self, command:str, cwd:str = BASE_DIR, show_output:bool = False) -> str|int:
    """
    Using the os.system() method execute the command (a string) in a sub-shell.
    This method is implemented by calling the standard C function system(), and has the same limitations.

    :param command str: the input command(s) to send to the system
    :return str: the returncode if output was shown or the output if it was not shown
    """
    if show_output:
      process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE)
      while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
          break
        if output:
          output = "  " + str(output.strip(), 'utf-8')
          self.append_log_cache([output, '\n'])
          print(output)
      return str(process.stdout.read(), 'utf-8')
    else:
      out = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        encoding='utf-8'
      )
      return out.stdout

  @sudo
  def sudo(self, command:str, cwd:str = BASE_DIR, show_output:bool = False, *args, **kwargs) -> str|int:
    """
    Using the console.input method combined with the sudo decorator we can correctly handle
    the use of sudo via the console library.
    """
    if command.strip().startswith('sudo ') and not command.strip().startswith('sudo -S '):
      command.replace('sudo ', 'sudo -S ', 1)
    if not command.strip().startswith('sudo'):
      command = 'sudo -S ' + command
    if len(kwargs['sudo_pass']) == 0:
      return console.input(command=command, cwd=cwd, show_output=show_output)
    return console.input(command=f'''echo {kwargs['sudo_pass']} | {command}''', cwd=cwd, show_output=show_output)

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
