#!C:\Overlord\.env\Scripts\python.exe
try:
  from sys import path
  from core.tools import tools
except ImportError:
  from os import system
  system('C:\Overlord\.env\Scripts\python.exe -m pip install -r core/requirements.txt')
from sys import path
from core.tools import tools
if 'C:\Overlord' not in path:
  path.insert(0, 'C:\Overlord');
from django.core.wsgi import get_wsgi_application;
application = get_wsgi_application();
tools.run()
