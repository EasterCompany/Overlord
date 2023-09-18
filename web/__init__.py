# web/__init__.py
#   automatically generated file
#   do not edit or remove
from os import makedirs
from os.path import exists

try:
  from . import settings
except ImportError:
  from core.tools.assets import settings
  from core.tools.commands.install import install_file
  install_file('settings.py', '/web', settings.BASE_DIR, log=False)
  try:
    from . import settings
  except ImportError as exception:
    print(exception)
    exit()

for _dir in settings.STATICFILES_DIRS:
  if not exists(_dir):
    makedirs(_dir, exist_ok=True)
