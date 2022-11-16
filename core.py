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
  command = lambda x: len(argv) > 1 and argv[1] == x

  if command('createsuperuser') or command('createadmin'):
    create_super_user()
  elif command('createuser'):
    create_user()
  elif command('tools'):
    tools.run()
  else:
    from core.library import execute_from_command_line
    execute_from_command_line(argv)
