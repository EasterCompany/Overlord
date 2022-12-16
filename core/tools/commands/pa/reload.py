# Overlord library
from .api import domain, fetch_api
from core.library.console import console


def request():
    print(f'\nReloading {domain} ...\n')
    data = fetch_api('webapps', args=(domain, 'reload'), method='POST')
    print('STATUS:', console.status(data['status']))
