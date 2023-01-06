# web/clients.py
#   automatically generated file
#   do not edit or delete
from core.library import console

try:
  from clients import (
  __installed_clients_tag__
  )
except ImportError as client_import_error:
  console.out(
    f"    {client_import_error}\n    your server.json 'INDEX' configuration may be set incorrectly.",
    "yellow"
  )

installed_clients = [
__installed_clients_tag__
]

for client in installed_clients:
  try:
    client.Client()
  except Exception as client_init_error:
    print(client_init_error)
