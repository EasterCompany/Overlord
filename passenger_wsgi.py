# SYSTEM IMPORTS
import os
import sys
from website import wsgi

# SET WORKING DIRECTORY
sys.path.insert(0, os.path.dirname(__file__))

# DEFINE WEB APPLICATION
application = wsgi
