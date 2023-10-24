# Standard library
import sys
import subprocess
from os import system
from threading import Thread
# Overlord library
from web.settings import BASE_DIR, SECRET_DATA
from core.library import console
from core.tools.library import fix_migrations
from django.core.management import call_command


# Server thread function
def _server(start:bool = True, migrate:bool = False, collectstatic:bool = False) -> None:
    """
    Runs a server on a thread which can be isolated from the main program and includes
    options to migrate the database or collect static files during the boot process

    :param start bool: whether the server should start after boot process
    :param migrate bool: whether the database should migrate during boot process
    :param collectstatic bool: whether the server should collect static files during boot process
    :return None:
    """

    if migrate:
        console.log("Migrating database")
        call_command('makemigrations')
        fix_migrations.apply_fixtures()
        call_command('migrate')
        console.log("Successfully migrated database")

    if collectstatic:
        call_command('collectstatic', '--noinput', '-i admin')

    if start:
        system(f"cd {BASE_DIR} && {sys.executable} core.py runserver 0.0.0.0:{SECRET_DATA['LOCAL_PORT']}")


# Server database migration shortcut
migrate_database = lambda: _server(start=False, migrate=True, collectstatic=False)

# Server collect static files shortcut
collect_staticfs = lambda: _server(start=False, migrate=False, collectstatic=True)


def run() -> None:
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


def start() -> None:
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


def install_requirements() -> None:
    """
    Install basic python package requirements
    """
    console.out("\n Installing Essential Python Requirements", "yellow")
    print("---------------------------------------------")
    subprocess.run(f"{sys.executable} -m pip install -r ./core/requirements.txt", shell=True, cwd=BASE_DIR)


def install_requirements_dev() -> None:
    """
    Install developer python package requirements
    """
    console.out("\n Installing Developer Python Requirements", "yellow")
    print("---------------------------------------------")
    subprocess.run(f"{sys.executable} -m pip install -r ./core/requirements.dev", shell=True, cwd=BASE_DIR)
