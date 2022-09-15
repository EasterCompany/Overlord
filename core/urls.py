# Standard library
import json
# Overlord library
from .library import api
from core.library import path
from web.settings import SECRET_DATA, SERVER_DATA, CLIENT_DATA, BASE_DIR


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

    return api.success()

  return api.error()


URLS = [

  # --- STATUS ---

  path(
    "api/status",
    lambda req, *args, **kwargs: api.std(api.OK, "API Endpoint Root"),
    name="Check API Status"
  ),

  path(
    "api/verify",
    lambda req, *args, **kwargs: \
      api.std(api.OK, "Verified") if req.GET.get("key") == SECRET_DATA['PUBLIC_KEY'] else api.error(),
    name="Check API Key Status"
  ),

  # --- CLIENTS ----

  path(
    "api/clients",
    view_local_clients,
    name="View This Servers Clients"
  ),

  path(
    "api/updatePrimaryClient",
    update_primary_client,
    name="Update This Servers Primary Client"
  ),

]
