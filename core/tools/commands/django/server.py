# Standard library
import sys
import subprocess
from os import system
from threading import Thread
# Overlord library
from web.settings import BASE_DIR
from core.library import console
from django.core.management import call_command


# Server thread function
def _server(start=True, migrate=False, collectstatic=False):

    if migrate:
        console.log("Migrating database")
        call_command('makemigrations')
        call_command('migrate')
        console.log("Successfully migrated database")

    if collectstatic:
        call_command('collectstatic', '--noinput', '-i admin')

    if start:
        system(f"{BASE_DIR}/core.py runserver 0.0.0.0:8000")


# Server database migration shortcut
migrate_database = lambda: _server(start=False, migrate=True, collectstatic=False)

# Server collect static files shortcut
collect_staticfs = lambda: _server(start=False, migrate=False, collectstatic=True)


def run():
    """
    Run process on the main thread
    """
    thread = Thread(
        None,
        _server,
        'django-server',
        ()
    )
    migrate_database()
    return thread.run()


def start():
    """
    Run new thread in the background
    """
    thread = Thread(
        None,
        _server,
        'django-server',
        ()
    )
    _server(start=False, migrate=True, collectstatic=False)
    return thread.start()


def install_requirements():
    """
    Install basic python package requirements
    """
    console.out("\n Installing Essential Python Requirements", "yellow")
    print("---------------------------------------------")
    subprocess.run(f"{sys.executable} -m pip install -r ./core/requirements.txt", shell=True, cwd=BASE_DIR)


def install_requirements_dev():
    """
    Install developer python package requirements
    """
    console.out("\n Installing Developer Python Requirements", "yellow")
    print("---------------------------------------------")
    subprocess.run(f"{sys.executable} -m pip install -r ./core/requirements.dev", shell=True, cwd=BASE_DIR)
