# web/urls.py
#   automatically generated file
#   do not edit or delete

# Django library
from django.conf import settings
from django.conf.urls.static import static

# Overlord library
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
# then the original home path will overwrite the app2 path and then the app2 client won't be able to be served

installed_clients = [
__installed_clients_tag__
]

# Url Patterns are for django
# this variable determines which endpoint the user has requested
# and is accessed only by the Django server on development or production builds
#
#   `/static/` takes priority over all other apps
#   index page hosted on `/` should always be loaded last in the load order of `installed_clients`
#   if the index page is loaded prior to other applications - the preceding clients will be overwritten by the index
#
# ---
# For example; outside of the Overlord framework we would have to manually specify the
# path for each client or api endpoint eg; path('user-login', user.login, name="user login")

urlpatterns = (
    [make_django_urls(client) for client in installed_clients] +
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
    API.URLS +
    CORE.URLS
)
