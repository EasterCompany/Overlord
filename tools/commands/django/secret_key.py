from json import loads, dump
from cryptography.fernet import Fernet


def new(project_path='.'):
    print('Generating new secret key...')
    new_key = Fernet.generate_key()

    with open(project_path + '/.config/secret.json') as old_file:
        data = loads(old_file.read())
        data['SERVER_KEY'] = new_key.decode('utf-8')

    with open(project_path + '/.config/secret.json', 'w') as conf_file:
        dump(
            data,
            conf_file,
            indent=2
        )

    print(new_key)
    return new_key
