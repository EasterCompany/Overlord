# web/urls.py
#   automatically generated file
#   do not edit or delete

# Django library
from django.conf import settings
from django.conf.urls.static import static

# Overlord library
from core.library import path
from core.library.url import make_django_urls

# Overlord api
from api import urls as API
from core import urls as CORE

# Overlord clients
from clients import (
__installed_clients_tag__
)

# Installed Clients are clients that are available to be served over HTTP(S)
# the load order is determined by the position of the client in this list of installed clients
# if an app 'higher' in the load order uses the same root path as a client 'lower' in the load order
# it's path will overwrite the ones below it.
# ---
# For example; if you have a `home` client installed which is served on re_path(r'.*')
# and a secondary client eg; `app2` installed which is served on re_path(r'app2.*')
# then the original home path will overwrite the app2 path and the app2 client won't be able to be served

installed_clients = [
__installed_clients_tag__
]

# Core web files are generated for each client within your clients directory
# however; currently only the index client supports them in production.

index = installed_clients[-1].Client()
index_app_files = [
    path('robots.txt', index.robots, name="Application Robots File"),
    path('manifest.json', index.manifest, name="Application Manifest File"),
    path('asset-manifest.json', index.assets, name="Application Assets File"),
]

if index.PWA: index_app_files = index_app_files + [
    path('service-worker.js', index.service_worker, name="Application Service Worker"),
    path('service-worker.js.map', index.service_worker_map, name="Application Service Worker Map"),
]

# Url Patterns are for django
# this variable determines which endpoint the user has requested
# and is accessed only by the Django server on development or production builds
#
#   `/static/` & `/api/` take priority over all other apps
#    as well as the index clients robots, manifest & service worker files.
#   the index client hosted on `/` should always be loaded last in the load order of `installed_clients`
#   if the index client is loaded prior to other applications - the preceding clients will be overwritten by the index
#
# ---
# For example; outside of the Overlord framework we would have to manually specify the
# path for each client or api endpoint eg; path('user-login', user.login, name="user login")

urlpatterns = (
    index_app_files +
    [make_django_urls(client) for client in installed_clients] +
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
    API.URLS +
    CORE.URLS
)
