# Standard library
from os import system
from threading import Thread
from sys import executable, path

# Django library
from web import settings


# Server thread function
def _server(start=True, migrate=False, collectstatic=False):

    def cmd(_cmd):
        system("{python} {dir}/run.py {command}".\
            format(python=executable, dir=path[0], command=_cmd)
        )

    if migrate:
        cmd('makemigrations')
        cmd('migrate')

    if collectstatic:
        cmd('collectstatic --noinput -i admin')
        print('')

    if start:
        if settings.SERVER_DATA['STANDALONE']:
            cmd('runserver 3000')
        else:
            cmd('runserver')


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
