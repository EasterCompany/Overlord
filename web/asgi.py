#  web/asgi.py
#    automatically generated file
#    do not edit or remove
from api.routing import urlpatterns
from core.library import asgi_with_channels_interface

application = asgi_with_channels_interface(urlpatterns)
