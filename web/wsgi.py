# Standard Library
import os

# Django library
from django.core.wsgi import get_wsgi_application

# WSGI Configurations
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
application = get_wsgi_application()
