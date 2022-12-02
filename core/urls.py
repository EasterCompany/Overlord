# Standard library
import os
import json
# Overlord library
from core.library import path, api
from core.library.console import Console
from core.tools.commands.external import external_command
from web.settings import SECRET_DATA, SERVER_DATA, CLIENT_DATA, BASE_DIR, LOGGER_DIR


def view_local_clients(req, *args, **kwargs):
  """
  Returns a json object containing the primary client & secondary clients list

  :param pid str: panel identifier
  :return api data: { primaryClient: <str>, secondaryClients: <list> }
  """
  api_key = req.GET.get("key")

  if api_key == SECRET_DATA["PUBLIC_KEY"]:
    primary_client = SERVER_DATA["INDEX"]
    secondary_clients = []

    for client in CLIENT_DATA:
      if client != primary_client:
        secondary_clients.append(client)

    return api.data({
      "primaryClient": primary_client,
      "secondaryClients": secondary_clients
    })

  return api.error()


def update_primary_client(req, *args, **kwargs):
  """
  Consumes the input and updates this servers "index" setting, also known as the Primary Client

  :param pid str: panel identifier
  :return api status:
  """
  api_key = req.GET.get("key")
  new_index = api.get_body(req)

  if api_key == SECRET_DATA["PUBLIC_KEY"]:
    _path = f"{BASE_DIR}/.config/server.json"

    with open(_path) as server_data_file:
      data = json.loads(server_data_file.read())

    data["INDEX"] = new_index

    with open(_path, 'w+') as conf_file:
      json.dump(
        data,
        conf_file,
        indent=2
      )

    Console.log(f"User {api.get_user(req)} updated the primary client to {new_index}")
    return api.success()

  return api.error()


def view_local_logs():
  """
  Read the local logging file and return it in a consumable HTML based format

  :return api data: { logs: <str> }
  """
  if not os.path.exists(LOGGER_DIR):
    return api.error()

  with open(LOGGER_DIR, 'r') as log_file:
    return api.data({ 'logs': log_file.read() })


URLS = [

  # --- STATUS ---

  path(
    "api/o-core/status",
    lambda req, *args, **kwargs: api.std(api.OK, "API Endpoint Root"),
    name="Check API Status"
  ),

  # --- KEY VERIFICATION ---

  path(
    "api/o-core/verify",
    lambda req, *args, **kwargs: \
      api.std(api.OK, "Verified") if req.GET.get("key") == SECRET_DATA['PUBLIC_KEY'] else api.error(),
    name="Check API Key Status"
  ),

  # --- WEB CONSOLE ---

  path(
    "api/o-core/logs",
    lambda req, *args, **kwargs: \
      view_local_logs() if req.GET.get("key") == SECRET_DATA['PUBLIC_KEY'] else api.error(),
    name="View API Logs"
  ),

  path(
    "api/o-core/external-command",
    external_command,
    name="Use External Command"
  ),

  # --- CLIENTS ----

  path(
    "api/o-core/clients",
    view_local_clients,
    name="View This Servers Clients"
  ),

  path(
    "api/o-core/updatePrimaryClient",
    update_primary_client,
    name="Update This Servers Primary Client"
  ),

]
