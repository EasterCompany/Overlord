# Overlord library
from .api import domain, fetch_api
from core.library.console import console


def request():
    print(f'\nReloading {domain} ...\n')

    data = fetch_api('webapps', args=(domain, 'reload'), method='POST')
    msg = "Reloaded Server." if data['status'] == "OK" else None
    console.status(data['status'], msg)

    if 'data' in data and data['data'] == "[500] Internal server error.":
        print('REASON:', console.output(data['data'], 'red'))
        print('\nAre you using the correct authentication method?')
