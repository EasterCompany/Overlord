# Overlord library
from .api import domain, server
from core.tools.library import console


def request():
    print(f'\nChecking {domain} ...\n')
    data = server('status')
    status = data['status'] if data['status'] != 200 else 'OK'
    print('STATUS:', console.colour_status_code(status))
