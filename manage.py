import pytest
from sys import argv, executable
from os import chdir, system, environ, path
from threading import Thread

BASE_DIR = path.dirname(path.abspath(__file__))


def main():
    environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise exc.ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    execute_from_command_line(argv)


def client(build=False):
    chdir('./client')
    if build:
        system('npm run build')
    else:
        system('npm run start')
    chdir(BASE_DIR)


def server(start=True, migrate=False):

    def run(_cmd):
        system("{python} {dir}/manage.py {command}".\
            format(python=executable, dir=BASE_DIR, command=_cmd)
        )

    if migrate:
        run('makemigrations')
        run('migrate')

    if start:
        run('runserver')


if __name__ == '__main__':
    serverThread = Thread(None, server, 'django', ())
    clientThread = Thread(None, client, 'react', ())

    if len(argv) > 1 and argv[1] == 'server':
        serverThread.run()

    elif len(argv) > 1 and argv[1] == 'client':
        clientThread.run()

    elif len(argv) > 1 and argv[1] == 'test':
        pytest.main(['./'])

    elif len(argv) > 1 and argv[1] == 'run':
        server(start=False, migrate=True)
        if pytest.main(['./']):
            exit(1)
        else:
            serverThread.start()
            clientThread.run()

    elif len(argv) > 1 and argv[1] == 'start':
        server(start=False, migrate=True)
        if pytest.main(['./']):
            exit(1)
        else:
            client(build=True)
            system('clear')
            serverThread.run()

    elif len(argv) > 1 and argv[1] == 'build':
        client(build=True)

    else:
        main()
