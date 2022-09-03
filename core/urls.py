# Overlord
from .library import api
from django.urls import path
from web.settings import SECRET_DATA, SERVER_DATA, CLIENT_DATA


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

]
