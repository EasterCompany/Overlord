#! /usr/bin/python3

# Standard library
from sys import argv
from os import environ
# Overlord library
from core import create_super_user, create_user
from core.tools import tools
from core.library import get_wsgi_application

if __name__ == '__main__':
  environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
  application = get_wsgi_application()

  if len(argv) >= 1 and argv[1] == 'createsuperuser':
    create_super_user()
  elif len(argv) >= 1 and argv[1] == 'createuser':
    create_user()

  elif len(argv) > 1 and argv[1] == 'tools':
    # Overlord Command Line Interface Tools
    tools.run()

  else:
    # Default Django Command Line Interface Tools
    from core.library import execute_from_command_line
    execute_from_command_line(argv)
