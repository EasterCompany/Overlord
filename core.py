#! /usr/bin/python3
from os import system, path
from shutil import rmtree
from sys import argv, executable

if __name__ == '__main__':

  if argv[1] == 'install':
    root = __file__.replace('core.py', '')
    env_path = __file__.replace('core.py', '.env')

    if path.exists(env_path):
      i = input("\nA virtual environment already exists for this project, would you like delete it? (Y/n): ")
      if not i.lower() == 'y':
        exit()
      rmtree(env_path)
      print('')

    system(f"cd {root} && {executable} -m venv .env")
    system(f"cd {root} && {root}.env/bin/python -m pip install -r core/requirements.txt")
    system(f"cd {root} && {root}.env/bin/python {root}core.py tools install")
    exit()

  from core import create_user
  from core.tools import tools
  from core.library import console, asgi_interface

  application = asgi_interface()
  command = lambda x: len(argv) > 1 and argv[1] == x

  if command('createsuperuser') or command('createadmin'):
    create_user(99)
  elif command('createuser'):
    create_user(1)
  elif command('tools'):
    tools.run()
  else:
    from core.library import execute_from_command_line
    execute_from_command_line(argv)
    if len(argv) == 1 or argv[-1] == './core.py': console.out(
      '\n[WARNING]\n    You are interacting with an Overlord underlayer called Django\n'
      '    Even if you know what you are doing, please avoid this if possible.\n',
      'yellow'
    )
