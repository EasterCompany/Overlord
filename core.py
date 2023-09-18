import platform
import subprocess
from pathlib import Path
from shutil import rmtree
from sys import argv, executable

if __name__ == '__main__':

  if argv[1] == 'install':
    is_windows = platform.system() == "Windows"
    root = Path(__file__.replace('core.py', ''))
    env_path = Path(__file__.replace('core.py', '.env'))
    env_exe = f"{env_path}\Scripts\python.exe" if is_windows else f"{env_path}/bin/python"

    if env_path.exists():
      i = input("\nA virtual environment already exists for this project, would you like to delete it? (Y/n): ")
      if not i.lower() == 'y':
        exit()
      rmtree(env_path)

    subprocess.run(f'''"{executable}" -m venv .env''', shell=True, cwd=root)
    subprocess.run(f'''"{env_exe}" -m pip install --upgrade pip''', shell=True, cwd=root)
    subprocess.run(f'''"{env_exe}" -m pip install -r core/requirements.txt''', shell=True, cwd=root)
    if is_windows:
      subprocess.run(f'''"{env_exe}" -m pip install pyreadline3''', shell=True, cwd=root)
    subprocess.run(f'''"{env_exe}" "{root}/core.py" tools install''', shell=True, cwd=root)
    exit()

  from core import create_user
  from core.tools import tools
  from core.library import console, asgi_interface

  application = asgi_interface()
  command = lambda x: len(argv) > 1 and argv[1] == x

  if command('createadmin'):
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
