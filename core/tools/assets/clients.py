# web/clients.py
#   automatically generated file
#   do not edit or delete

try:
  from clients import (
  __installed_clients_tag__
  )
except ImportError as client_import_error:
  print(f"    {client_import_error}\n    is your server 'index' configuration set correctly?")

installed_clients = [
__installed_clients_tag__
]

for client in installed_clients:
  try:
    client.Client()
  except Exception as client_init_error:
    print(client_init_error)
