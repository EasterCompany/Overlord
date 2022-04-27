# Standard Library
from sys import path
from json import loads
from time import sleep
from shutil import rmtree
from os.path import exists
from threading import Thread
from datetime import datetime
from os import chdir, system, rename, remove

# Overlord-Web import
from web import settings

# Overlord-Tools import
from tools.library import console

# Variable app meta data
meta_data = {
    'time_of_last_build': datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
}


# Client build meta data
def update_client_meta_data(app_data):
    # Read index.html file content
    index_path = app_data['static'] + '/index.html'

    # Pass if build doesn't exist
    if not exists(index_path):
        return False

    # Read Content
    with open(index_path) as index_file:
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
        system('npm run build')
        update_client_meta_data(app_data)
    elif 'start' in app_data:
        system('npm run start')
    chdir(path[0])


# Create client thread
new_client = lambda app_name, app_data, build: Thread(
    None,
    client,
    app_name + '-client',
    (app_data, build)
)

# All clients data from config file
if exists(path[0] + '/.config/clients.json'):
    with open(path[0] + '/.config/clients.json') as clients_file:
        clients_json = loads(clients_file.read())
else:
    clients_json = {}


# Install client
def install(target=None):

    def run_install(client_path):
        chdir(client_path)
        system('npm install')

    if target is None:
        for client in clients_json:
            print('\n', client, '----------------')
            run_install(clients_json[client]['src'])
        print()
    else:
        run_install(clients_json[target]['src'])

    return chdir(path[0])


# Run client
def run(name, build, new_thread):
    if name not in clients_json:
        print('\n    Client `%s` does not exist\n' % name), exit()
    client_data = clients_json[name]
    thread = new_client(name, client_data, build)
    if new_thread:
        thread.start()              # Start thread
        sleep(3)                    # Give NPM time to collect package.json
        return chdir(path[0])       # Return to root directory
    return thread.run()             # ELSE: Run on main thread


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
    for client in clients_json:
        run(client, build=True, new_thread=False)


# Create new client
def create(name):

    # Make directory checks
    if exists('clients/' + name):
        return print("\n ABORTED: %s already exists \n" % name)

    # Fetch template from github
    system('''
            echo '' && cd clients &&
            git clone git@github.com:EasterCompany/PWA-Template.git {name} &&
            cd .. && echo ''
        '''.format(name=name)
    )

    # De-git repository
    print('De-git repository...')
    remove('clients/{name}/.gitignore'.format(name=name))
    rmtree('clients/{name}/.git'.format(name=name))

    # Update meta_data
    print('Update index data...')
    rename(
        'clients/{name}/public/static/app-name'.format(name=name),
        'clients/{name}/public/static/{name}'.format(name=name)
    )

    with open('clients/{name}/public/index.html'.format(name=name)) as index_content:
        content = index_content.read()
        content = content.replace('{#app_name#}', name)
        with open('clients/%s/public/index.html' % name, 'w') as new_file:
            new_file.write(content)

    # Update manifest.json
    print('Update manifest data...')
    with open('clients/{name}/public/manifest.json'.format(name=name)) as manifest:
        content = manifest.read()
        content = content.replace('app-name', name)
        with open('clients/%s/public/manifest.json' % name, 'w') as new_file:
            new_file.write(content)

    # Update package.json
    print('Update package data...')
    with open('clients/{name}/package.json'.format(name=name)) as package:
        content = package.read()
        content = content.replace('app-name', name)
        with open('clients/%s/package.json' % name, 'w') as new_file:
            new_file.write(content)

    # Update environment variables
    print('Update environment data...\n')
    clients_data = {}
    next_port = 8100
    with open('.config/clients.json') as clients_json:
        clients_data = loads(clients_json.read())
        next_port += len(clients_data)
    with open('clients/%s/.env' % name, 'w+') as env_file:
        env_file.write('PORT=%s' % next_port)

    print(console.col(' Done!', 'green'))
    print('\ninstall this app with `./o install -client -%s` \n' % name)


# Module error message
def error_message():
    return print('''
    `CLIENTS` tool requires atleast one argument beggining with `-`

        ./o runclient -client_name
        ./o build -client_name
        ./o create -client_name

    or use -all to effect all clients

        ./o runclient -all
        ./o build -all
    ''')
