from sys import path as _path
from os.path import exists as _exists

if _exists(_path[0] + '/.config/secret.json'):
    from . import api, apps, \
        consoles, cpu, \
        reload, tasks, upgrade, status
