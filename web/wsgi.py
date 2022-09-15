#  web/wsgi.py
#    automatically generated file
#    do not edit or remove

# Standard Library
import os
# Overlord library
from core.library import get_wsgi_application

# WSGI Configurations
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
application = get_wsgi_application()
