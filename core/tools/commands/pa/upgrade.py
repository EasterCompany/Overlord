# Overlord library
from .api import domain, fetch_domain
from core.tools.library import console


def request():
    print('\nUpgrading', domain, '...\n')
    data = fetch_domain('upgrade')
    print('status:', console.colour_status_code(data['status']), '\n')
    if data['status'] != 'OK': exit()
