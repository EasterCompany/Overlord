# Overlord library
from .api import domain, server
from core.library import console


def request():
    print(f'\nChecking {domain} ...\n')

    data = server('status')
    if 'error' in data:
        msg = "SERVER IS DOWN!"
    else:
        msg = "Server Responded" if data['status'] == "OK" else None
        console.status(data['status'], msg)

    if 'error' in data:
        console.status(404, msg)
    elif 'data' in data and data['data'] == "[500] Internal server error.":
        print('REASON:', console.out(data['data'], 'red'))
        print('\nAre you using the correct authentication method?')

    return data
