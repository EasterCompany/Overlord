# Standard library
import subprocess
from json import loads
from time import sleep
from shutil import rmtree
from os.path import exists
from threading import Thread
from datetime import datetime
from os import chdir, system, rename, remove, getcwd
# Overlord library
from ..install import (
    __init_config_directory__,
    __init_logs_directory__,
    make_clients_config,
    make_server_config
)
from ..node.share import __update_shared_files__
from core.library.console import console
from web.settings import BASE_DIR

# Variable app meta data
meta_data = {
    'time_of_last_build': datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
}


# Client build meta data
def update_client_meta_data(app_data):
    # Read index.html file content
    if BASE_DIR in app_data['static']:
        index_path = f"{app_data['static']}/index.html"
    else:
        index_path = f"{BASE_DIR}{app_data['static']}/index.html"

    # ERROR handling when index.html is not generated
    if not exists(index_path):
        index_path = index_path.replace('/index.html', '/index')

    # Read Content
    with open(index_path, 'r') as index_file:
        index_file_content = index_file.read()

    # Iterate over all variable meta data
    for tag in meta_data:
        index_file_content = \
            index_file_content.replace('{#' + tag + '#}', meta_data[tag])

    # Write new index.html file content
    with open(index_path, 'w+') as index_file:
        index_file.write(index_file_content)

    # Rename html tag from built index file
    rename(index_path, index_path.replace('.html', ''))

    # Remove status code specific html files
    if exists(app_data['static'] + '/200.html'):
        remove(app_data['static'] + '/200.html')
    if exists(app_data['static'] + '/404.html'):
        remove(app_data['static'] + '/404.html')
    return True


# Client thread function
def client(app_data, build=False):
    chdir(app_data['src'])
    if build and 'build' in app_data:
        console.log(f"    Installing packages")
        #system('npm install')
        install_process = subprocess.run(
            ["npm", "install"],
            bufsize=1,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            universal_newlines=True
        )
        console.log(install_process.stdout)
        console.log(f"    Optimizing for production")
        #system('npm run build')
        build_process = subprocess.run(
            ["npm", "build"],
            bufsize=1,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            universal_newlines=True
        )
        console.log(build_process.stdout)
        console.log(f"    Updating meta data")
        update_client_meta_data(app_data)
    elif not build and 'start' in app_data:
        system('npm run start')
    chdir(BASE_DIR)


# Create client thread
new_client = lambda app_name, app_data, build: Thread(
    None,
    client,
    app_name + '-client',
    (app_data, build)
)

clients_json = {}


def update_client_json():
    global clients_json
    # All clients data from config file
    if exists(BASE_DIR + '/.config/clients.json'):
        with open(BASE_DIR + '/.config/clients.json') as clients_file:
            clients_json = loads(clients_file.read())
    else:
        clients_json = {}
    return clients_json


update_client_json()


# Install client
def install(target=None):

    def run_install(client_path):
        chdir(client_path)
        system('npm install')

    update_client_json()

    if target is None:
        for client in clients_json:
            print('\n', client, '----------------')
            run_install(clients_json[client]['src'])
        print('')
    else:
        run_install(clients_json[target]['src'])
        print('')

    return chdir(BASE_DIR)


# Run client
def run(name, build, new_thread):
    if name not in clients_json:
        return print(f'\n    Client `{name}` does not exist\n')
    client_data = clients_json[name]
    if new_thread:
        thread = new_client(name, client_data, build)
        thread.start()
        sleep(3)
        return chdir(BASE_DIR)
    return client(client_data, build)


# Run all clients on a separate thread except the last one
def run_all(none_on_main_thread=False):
    for index, client in enumerate(clients_json):
        if index < len(clients_json) - 1 or none_on_main_thread:
            run(client, build=False, new_thread=True)
        else:
            run(client, build=False, new_thread=False)
    sleep(5)
    system('clear')
    return print('Running all clients...\n')


# Build specific client on the main thread
def build(name):
    return run(name, build=True, new_thread=False)


# Build all clients on the main thread
def build_all():
    console.log("Building all clients ...")
    for client in clients_json:
        console.log(f"  {client}")
        run(client, build=True, new_thread=False)
    console.log("Successfully built all clients")


# Create new client
def create(name, native=False, custom_repo=None):

    def download_repo(repo_link, name):
        return system(f'''
            echo '' && cd clients &&
            git clone {repo_link} {name} &&
            cd .. && echo ''
        ''')

    def update_overlord_configuration():
        from core.library import url

        # Setup environment
        __init_config_directory__()
        __init_logs_directory__()

        # Default environment configuration
        client_data = make_clients_config(BASE_DIR)
        server_data = BASE_DIR + '/.config/server.json'

        if exists(server_data):
            with open(server_data) as server_data_file:
                server_data = loads(server_data_file.read())
        else:
            server_data = make_server_config(BASE_DIR)

        # Default start-up behavior
        __update_shared_files__()
        load_order = url.make_client_load_order(client_data, server_data['INDEX'])
        url.write_django_urls(load_order, BASE_DIR + '/web/urls.py')

    # Make directory checks
    if exists(f'clients/{name}'):
        return print(
            console.output('\n[ABORTED]', 'red') + f" client with name '{name}' already exists.\n"
        )

    # Fetch react-native app template from github
    if native:
        print("\nDownloading native-client template...")
        download_repo('git@github.com:EasterCompany/Overlord-Native-Client.git', name)

    # Fetch custom or existing client template from any SSH or HTML based repository
    elif custom_repo is not None:
        print("\nDownloading custom-client template...")
        download_repo(custom_repo, name)
        print(console.output(f'Successfully created a custom client: {name} !', 'green'))
        print(f'To install your client use this command `./o install -{name}`\n')
        return update_overlord_configuration()

    # Fetch default react-web template from github
    else:
        print("\nDownloading web-client template...")
        download_repo('git@github.com:EasterCompany/Overlord-React-Client.git', name)

    # De-git repository
    print('De-git repository...')
    rmtree(f'clients/{name}/.git')

    # Update meta_data
    if exists(f'clients/{name}/public/static/app-name'):
        print('Update index data...')
        rename(f'clients/{name}/public/static/app-name', f'clients/{name}/public/static/{name}')

    if native:
        # Update native app.json
        print('Update app data...')
        with open(f'clients/{name}/app.json') as package:
            content = package.read()
            content = content.replace('app-name', name.lower())
            with open(f'clients/{name}/app.json', 'w') as new_file:
                new_file.write(content)

    else:
        # Update index.html
        with open(f'clients/{name}/public/index.html') as index_content:
            content = index_content.read()
            content = content.replace('{#app_name#}', name)
            with open(f'clients/{name}/public/index.html', 'w') as new_file:
                new_file.write(content)

        # Update manifest.json
        print('Update manifest data...')
        with open(f'clients/{name}/public/manifest.json') as manifest:
            content = manifest.read()
            content = content.replace('app-name', name)
            with open(f'clients/{name}/public/manifest.json', 'w') as new_file:
                new_file.write(content)

    # Update package.json
    print('Update package data...')
    with open(f'clients/{name}/package.json') as package:
        content = package.read()
        content = content.replace('app-name', name)
        with open(f'clients/{name}/package.json', 'w') as new_file:
            new_file.write(content)

    # Update environment variables
    print('Update environment data...\n')
    clients_data = {}
    next_port = 8100
    with open('.config/clients.json') as clients_json:
        clients_data = loads(clients_json.read())
        next_port += len(clients_data)
    with open(f'clients/{name}/.env', 'w+') as env_file:
        env_file.write('PORT=%s' % next_port)

    update_overlord_configuration()

    print(console.output(f'Successfully created a web client: {name} !', 'green'))
    print(f'To install your client use this command `./o install -{name}`\n')


# Module error message
def error_message():
    return print('''
    `CLIENTS` tool requires at least one argument beginning with `-`

        ./o runclient -client_name
        ./o build -client_name
        ./o create -client_name

    or use -all to effect all clients

        ./o runclient -all
        ./o build -all

    to create a native client use the `-native` argument first

        ./o create -native -client_name
    ''')
