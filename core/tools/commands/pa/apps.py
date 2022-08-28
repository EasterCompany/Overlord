# Local app imports
from .api import fetch_api


def display():
    data = fetch_api('webapps')
    print('\n', ':------------ WEBAPP INFO -----------:\n')
    for app in data:
        print(
            ' ', app['user'], '-',  app['id'], '\n',
            ' URL:', app['domain_name'], '\n',
            ' HTTPS:', app['force_https'], '\n',
            ' Python:', app['python_version'], '\n',
            ' Source:', app['source_directory'], '\n',
            ' Working:', app['working_directory'], '\n',
        )
    print(' :-------------------------------------:\n')
