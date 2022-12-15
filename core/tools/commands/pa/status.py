# Overlord library
from .api import domain, server
from core.library.console import console


def request():
    print(f'\nChecking {domain} ...\n')
    data = server('status')

    status = data['status']
    print('STATUS:', console.status(status))

    if 'data' in data and data['data'] == "[500] Internal server error.":
        print('REASON:', console.output(data['data'], 'red'))
        print('\nAre you using the correct authentication method?')
