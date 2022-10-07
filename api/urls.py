#  api/urls.py
#    automatically generated file
#    do not modify or remove

# Overlord API Endpoints
from api.eastercompany.urls import API as eastercompany

# Overlord Core Endpoints
from core.model.user.urls import API as ol__user
from core.model.jobs.urls import URLS as ol__jobs
from core.model.posts.urls import URLS as ol__posts
from core.model.recipe.urls import API as ol__recipe

# Generated Endpoints
URLS = ol__user.URLS + ol__jobs + ol__posts + ol__recipe.URLS + \
  eastercompany.URLS
