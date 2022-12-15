# Overlord library
from .api import domain, server
from core.tools.library.console import colour_status_code


def request():
    print(f'\nUpgrading {domain} ...\n')
    data = server('deploy')
    print('STATUS:', colour_status_code(data['status']))
