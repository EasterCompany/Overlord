from json import loads, dump
from django.core.management.utils import get_random_secret_key


def new(project_path='.'):
    print('Creating new secret key...')
    new_key = get_random_secret_key()

    with open(project_path + '/.config/secret.json') as old_file:
        data = loads(old_file.read())
        data['SERVER_KEY'] = new_key

    with open(project_path + '/.config/secret.json', 'w') as conf_file:
        dump(
            data,
            conf_file,
            indent=2
        )

    return print('Success!')
