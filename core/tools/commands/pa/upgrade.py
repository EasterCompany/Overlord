# Overlord library
from .api import domain, server
from core.library.console import console


def request():
    print(f'\nUpgrading {domain} ...\n')
    data = server('upgrade')
    msg = "Upgraded Server." if data['status'] == "OK" else None
    console.status(data['status'], msg)

    if 'data' in data and data['data'] == "[500] Internal server error.":
        console.output(data['data'], 'red')

    return data
