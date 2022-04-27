# Local app imports
from .api import fetch_api


def display():
    data = fetch_api('consoles')
    print('\n', ':-------- CONSOLE LIST --------:\n')
    for con in data:
        print(
            ' ', con['name'], '-',  con['id'], '\n',
            ' Type:', con['executable'], '\n'
        )
    print(' :------------------------------:\n')
