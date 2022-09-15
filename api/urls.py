#  api/urls.py
#    automatically generated file
#    do not modify or remove

# Overlord API Endpoints
from api.eastercompany.urls import API as eastercompany

# Overlord Core Endpoints
from core.models.user.urls import URLS as ol__user
from core.models.jobs.urls import URLS as ol__jobs
from core.models.posts.urls import URLS as ol__posts
from core.models.recipe.urls import API as ol__recipe

# Generated Endpoints
URLS = ol__user + ol__jobs + ol__posts + ol__recipe.URLS + \
  eastercompany.URLS
