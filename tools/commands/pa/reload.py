# Local app imports
from tools.library import console
from .api import domain, fetch_api


def request():
    print('\nReloading', domain, '...\n')
    data = fetch_api('webapps', args=(domain, 'reload'), method='POST')
    print('status:', console.colour_status_code(data['status']), '\n')
    if data['status'] != 'OK': exit()
