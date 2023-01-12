#! /usr/bin/python3

# Standard library
from os import environ
from sys import argv
# Overlord library
from core import create_super_user, create_user
from core.tools import tools
from core.library import console, get_wsgi_application

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
    if len(argv) == 1 or argv[-1] == './core.py': console.out(
      '\n[WARNING]\n    You are interacting with an Overlord underlayer known as Django\n'
      '    Even if you know what you are doing, please avoid this if possible.\n',
      'yellow'
    )
