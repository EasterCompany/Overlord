#  api/urls.py
#    automatically generated file
#    do not modify or remove

# Overlord API Endpoints
# __imports_tag__

# Overlord Core Endpoints
from core.model.user.urls import API as ol__user
from core.model.posts.urls import URLS as ol__posts

# Generated Endpoints
URLS = ol__user.URLS + ol__posts # __urls_tag__

# Generated Sockets
SOCKETS = [] # __sockets_tag__
