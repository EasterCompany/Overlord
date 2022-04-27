# Standard library
import requests
from os import getcwd
from json import loads
from os.path import exists

# GET CONFIGURATION SECRETS
if exists(getcwd() + '/.config/secret.json'):
    with open(getcwd() + '/.config/secret.json') as secret_file:
        secret_data = loads(secret_file.read())
else:
    secret_data = {
        'SECRET_KEY': '',
        'PA_USER_ID': '',
        'PA_API_KEY': '',
        'DOMAIN_URL': ''
    }

# SET HOST INFORMATION
username = secret_data['PA_USER_ID']
token = secret_data['PA_API_KEY']
domain = secret_data['DOMAIN_URL']
secret = secret_data['SECRET_KEY']


def fetch_api(api, args=None, method='GET'):
    if token == '':
        print('''
    `SERVER TOOLS` requires an API token &
    username in your .config/secret.json file
    '''
        )
        exit()
    if args is not None:
        args = '/'.join(args) + '/'
    else:
        args = ''
    if method == 'GET': func = requests.get
    elif method == 'POST': func = requests.post
    response = func(
        'https://eu.pythonanywhere.com/api/v0/user/{username}/{api}/{args}'.format(
            username=username,
            api=api,
            args=args
        ),
        headers={
            'Authorization': 'Token {token}'.format(token=token)
        }
    )
    if not response.status_code == 200:
        return print('Got unexpected status code {}: {!r}'.format(
                response.status_code,
                response.content
            )
        ), exit()
    return loads(response.content)


def fetch_domain(api, args=None, method='GET'):
    if domain == '' or secret == '':
        print('''
    `SERVER TOOLS` requires a target domain &
    secret key in your .config/secret.json file
    '''
        )
        exit()
    if args is not None:
        args = '/' + '/'.join(args) + '/'
    else:
        args = ''
    if method == 'GET': func = requests.get
    elif method == 'POST': func = requests.post
    response = func(
        '{domain}/api/olt/{api}{args}'.format(
            domain=domain,
            api=api,
            args=args
        ),
        headers={
            'secret': '{key}'.format(key=secret)
        }
    )
    if not response.status_code == 200 and not api == 'status':
        return print('Got unexpected status code {}: {!r}'.format(
                response.status_code,
                response.content
            )
        ), exit()
    elif api == 'status' and not response.status_code == 200:
        return {'status': response.status_code}
    return loads(response.content)


def error_message():
    return print('''
        `PA API` tools require a single argument beggining with `-`

        ./o server -apps
        ./o server -cpu
        ./o server -consoles
        ./o server -tasks
        ./o server -upgrade
    ''')
