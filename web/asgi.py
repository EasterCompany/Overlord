#  web/asgi.py
#    automatically generated file
#    do not edit or remove
from api.urls import SOCKETS
from core.library import asgi_with_channels_interface

application = asgi_with_channels_interface(SOCKETS)
