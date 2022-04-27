# Local app imports
from .api import domain, fetch_domain
from tools.library import console


def request():
    print('\nVerifying', domain, '...\n')
    data = fetch_domain('status')
    print('status:', console.colour_status_code(data['status']), '\n')
