# Overlord library
from core.tools.library import console
from .api import domain, fetch_api


def request():
    print(f'\nReloading {domain} ...\n')
    data = fetch_api('webapps', args=(domain, 'reload'), method='POST')
    print('STATUS:', console.colour_status_code(data['status']), '\n')
    if data['status'] != 'OK': exit()
