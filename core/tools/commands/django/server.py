# Standard library
from os import system
from threading import Thread
from sys import executable, path
# Overlord library
from web.settings import BASE_DIR
from django.core.management import call_command


# Server thread function
def _server(start=True, migrate=False, collectstatic=False):

    if migrate:
        call_command('makemigrations')
        call_command('migrate')

    if collectstatic:
        call_command('collectstatic', '--noinput', '-i admin')

    if start:
        system(f"{BASE_DIR}/core.py runserver")


# Server database migration shortcut
migrate_database = lambda: _server(start=False, migrate=True, collectstatic=False)

# Server collect static files shortcut
collect_staticfs = lambda: _server(start=False, migrate=False, collectstatic=True)


def run():
    # Server thread
    thread = Thread(
        None,
        _server,
        'django-server',
        ()
    )
    migrate_database()
    return thread.run()


def start():
    # Server thread
    thread = Thread(
        None,
        _server,
        'django-server',
        ()
    )
    _server(start=False, migrate=True, collectstatic=True)
    return thread.start()
