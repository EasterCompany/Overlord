# Overlord library
from core.library import path, include, exists, console


def make_django_urls(client):
    """
    Automatically generates the URL patterns for your project using your clients __init__.py file

    :param client obj: a client class object from an __init__ file found within a client directory
    :return obj: path object from the django.urls library containing the url pattern for that client
    """
    client = client.Client()
    endpoint = client.ENDPOINT
    return path(endpoint, include([client.URL]), name=client.NAME)


def make_client_load_order(client_data, index):
    """
    Automatically generates which order to import and install clients. Load order decides which clients
    get priority of their declared url paths. The INDEX client will always load last and overwrite
    all other client urls so it can maintain the root path (ie; "http://www.easter.company/")

    :param client_data dict: dictionary container the '.config/clients.json' file
    :param index str: the name of the client you wish to be the index of your project
    :return str: a str styled as a list of client names with indentation for being injected into 'web/urls.py'
    """
    load_order = str()

    for client in client_data:
        if not client == index:
            load_order += f"  {client},\n"

    if index is not None and index != "":
        return load_order + f"  {index}"
    return load_order


def write_django_urls(load_order, urls_file_path) -> None:
    """
    Automatically generates the 'web/urls.py' file by using the <make_django_urls> & <make_client_load_order>
    functions

    :param load_order str: the results of the <make_client_load_order> function
    :param urls_file_path str: the path to the 'web/urls.py' file
    """

    with open(urls_file_path) as urls_file:
        file_content = urls_file.read()

    with open(urls_file_path, 'w+') as urls_file:
        if load_order == str():
            file_content = file_content.replace(
                "from clients import (\n"
                "__installed_clients_tag__\n"
                ")", ""
            )
        urls_file.write(file_content.replace('__installed_clients_tag__', load_order))


def acquire_client_api(client:str, git_ssh:str, api_dir:str, no_tab:bool = False) -> dict:
    """
    Automatically acquires installs an API from a git ssh link

    :param client str: name of the target client
    :param git_ssh str: ssh link to the git repository
    :param api_dir str: the directory of the new api
    :return str: returns the import statements for this api
    """
    console.out(f"    Cloning API for '{client}'", end=" ...\r")
    console.input(f"git clone {git_ssh} {client}", cwd=api_dir, show_output=False)
    if no_tab:
        return console.out(f"✔️ Successfully cloned API for '{client}'              ", "green")
    return console.out(f"    ✔️ Successfully cloned API for '{client}'              ", "green")


def acquire_all_clients_api(client_data:dict, cwd:str = '.', no_tab:bool = False) -> None:
    """
    Automatically scan each client for any missing associated APIs which may have
    not already been installed

    :param client_data dict: a dictionary containing all the captured client data
    :param cwd str: current working directory of the server
    """
    statements = []
    for client in client_data:
        api_dir = f"{cwd}/api"
        if client_data[client]['api'] is not None:
            statements.append({
                'urls_import': f'from api.{client}.urls import API as __{client}__',
                'models_import': f'from api.{client}.tables import *',
                'urls_access': "+ \\" + f'\n  __{client}__.URLS'
            })
            if not exists(f"{api_dir}/{client}"):
                acquire_client_api(client, client_data[client]['api'], api_dir, no_tab)
    return statements


def write_api_urls(statements:list, cwd:str = '.') -> None:
    """
    Automatically generates the './api/urls.py' file from a template file within the
    './core/tools/assets/' directory

    :param cwd str: current project working directory
    :return None:
    """
    imports = []
    access = ""

    for client in statements:
        imports.append(client['urls_import'])
        access += client['urls_access']

    with open(f'{cwd}/core/tools/assets/api_urls.py', 'r') as temp_f, open(f'{cwd}/api/urls.py', 'w') as new_f:
        template = temp_f.read()
        template = template.replace('# __imports_tag__', '\n'.join(imports))
        template = template.replace('# __urls_tag__', access)
        new_f.write(template)


def write_api_models(statements:list, cwd:str = '.') -> None:
    """
    Automatically generates the 'api/models.py' file from a template file within the
    './core/tools/assets/' directory

    :param cwd str: current project working directory
    :return None:
    """
    imports = []

    for client in statements:
        imports.append(client['models_import'])

    with open(f'{cwd}/core/tools/assets/api_models.py', 'r') as temp_f, open(f'{cwd}/api/models.py', 'w') as new_f:
        template = temp_f.read()
        template = template.replace('# __imports_tag__', '\n'.join(imports))
        new_f.write(template)
