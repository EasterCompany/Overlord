# Overlord library
from .api import fetch_api
from core.library import console


def display():
    data = fetch_api('webapps')
    print('\n :----------------------- WEBAPP INFO ----------------------:\n')
    for app in data:

        name = app['domain_name'].split('www.')[1] if 'www.' in app['domain_name'] else app['domain_name']
        name = console.out(name, 'yellow')

        if app['force_https']:
            protocol = 'https'
        else:
            protocol = 'http'

        print(
            f"  {name} - {app['id']} \n",
            f"  URL: {protocol}://{app['domain_name']} \n",
            f"  HTTPS: {app['force_https']} \n",
            f"  Python: {app['python_version']} \n",
            f"  Source: {app['source_directory']} \n",
            f"  Working: {app['working_directory']} \n",
        )

    print(' :-----------------------------------------------------------:\n')
