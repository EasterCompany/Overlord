#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from _thread import start_new_thread


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def client():
    os.chdir('./client')
    os.system('npm run start')


def server():
    os.system('./manage.py runserver')


if __name__ == '__main__':
    if 'runclient' in sys.argv:
        start_new_thread(client, ())
        server()
    elif 'build' in sys.argv:
        os.chdir('./client')
        os.system('npm run build')
    else:
        main()
