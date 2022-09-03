# Overlord library
from core.library import client


class Client(client.WebClient):

  # Client.ENVIRONMENT [ local, staging, production... ]
  ENV = __file__.replace('__init__.py', '.env')

  # Client.NAME and directory name for this client source files should be identical
  NAME = 'e_panel'

  # Client.PORT by default will be automatically determined if PORT is None.
  # otherwise you can specify a port number as a string.
  PORT = '8100'

  # Client.PWA is a boolean which indicates whether or not to enable service workers
  PWA = False
