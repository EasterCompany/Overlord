#! /usr/bin/python3

# Standard library
from sys import argv
from os import environ

# Overlord library
from core.tools import tools

if __name__ == '__main__':
  if len(argv) > 1 and argv[1] == 'tools':
    tools.run()
  else:
    environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
    try:
      from core.library import execute_from_command_line
    except ImportError as exc:
      raise exc.ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
      )
    execute_from_command_line(argv)