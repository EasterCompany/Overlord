# web/__init__.py
#   automatically generated file
#   do not edit or remove

try:
    from . import settings

except ImportError:
    from core.tools.assets import settings
    from core.tools.commands.install import install_file
    install_file('settings.py', '/web', settings.BASE_DIR)

    try:
        from . import settings
    except ImportError as exception:
        print(exception)
        exit()
