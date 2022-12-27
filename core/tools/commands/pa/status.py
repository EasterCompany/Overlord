# Overlord library
from .api import domain, server
from core.library.console import console


def request():
    print(f'\nChecking {domain} ...\n')

    data = server('status')
    msg = "Server is responding." if data['status'] == "OK" else None
    console.status(data['status'], msg)

    if 'data' in data and data['data'] == "[500] Internal server error.":
        print('REASON:', console.output(data['data'], 'red'))
        print('\nAre you using the correct authentication method?')

    return data
