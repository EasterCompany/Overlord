# Import the raw settings file from Overlord-Tools if the installed version in the project directory
# is not found. This allows Overlord-Server to boot the installation using default settings process without crashing.

try:
    from . import settings

except ImportError:
    from tools.assets import settings
    from tools.commands.install import install_file
    install_file('settings.py', '/web', settings.BASE_DIR)

    try:
        from . import settings
    except ImportError:
        exit
