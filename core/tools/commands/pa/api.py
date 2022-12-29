# Standard library
import json
import requests
from os import getcwd
from os.path import exists

# GET CONFIGURATION SECRETS
if exists(getcwd() + '/.config/secret.json'):
    with open(getcwd() + '/.config/secret.json') as secret_file:
        secret_data = json.loads(secret_file.read())
else:
    secret_data = {
        'SERVER_KEY': '',
        'PA_USER_ID': '',
        'PA_API_KEY': '',
        'DOMAIN_URL': ''
    }

# SET HOST INFORMATION
username = secret_data['PA_USER_ID']
token = secret_data['PA_API_KEY']
domain = secret_data['DOMAIN_URL']
key = secret_data['PUBLIC_KEY']


def fetch_api(api, args=None, method='GET'):
    if token == '':
        return print(
    '''
    `SERVER TOOLS` requires a PA_API_KEY &
    PA_USER_ID in your .config/secret.json file
    ''')

    if args is not None:
        args = '/'.join(args) + '/'
    else:
        args = ''

    if method == 'GET': func = requests.get
    elif method == 'POST': func = requests.post

    response = func(
        f'https://eu.pythonanywhere.com/api/v0/user/{username}/{api}/{args}',
        headers={
            'Authorization': f'Token {token}'
        }
    )

    if not response.status_code == 200:
        return print('Got unexpected status code {}: {!r}'.format(
                response.status_code,
                response.content
            )
        )
    return json.loads(response.content)


def server(command:str):
    if domain == '' or key == '':
        return print(
    '''
    `SERVER TOOLS` requires a DOMAIN_URL &
    PUBLIC_KEY in your .config/secret.json file
    ''')
    url = f'https://{domain}/api/o-core/external-command'
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "command": command,
        "pub_key": key
    }
    response = requests.post(url, headers=headers, json=data)
    if not response.status_code == 200:
        return print(f'Got unexpected response code [ERROR {response.status_code}]:\n{response.content}\n')
    return json.loads(response.content)


def error_message():
    return print('''
    `SERVER` tools require a single argument beginning with `-`

    ./o server -apps
    ./o server -cpu
    ./o server -consoles
    ./o server -status
    ./o server -tasks
    ./o server -upgrade     (updates server-side source code)
    ./o server -reload      (reboots the server)
    ./o server -deploy      (upgrades and reloads the server)
    ''')
