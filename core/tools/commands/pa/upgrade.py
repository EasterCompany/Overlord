# Overlord library
from .api import domain, server
from core.library import console


def request():
    print(f'\nUpgrading {domain} ...\n')
    data = server('upgrade')
    msg = "Server Upgraded" if data['status'] == "OK" else None
    console.status(data['status'], msg)

    if 'data' in data and data['data'] == "[500] Internal server error.":
        console.out(data['data'], 'red')

    return data
