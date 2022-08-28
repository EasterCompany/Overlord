# Standard library
import json
import requests
from uuid import uuid1
# Overlord library
from api.user.tables import UserAuth
from api.user.controls import if_authorized
from api.admin.tables import AdminPanel
from core.library.api import get_arg, get_user, get_body, get_api_url, error


def get_user_panels(uuid):
  user = UserAuth.objects.filter(uuid=uuid).first()
  if ',' in user.panels:
    return user.panels.split(',')[:-1]
  return []


def get_panel_users(pid):
  panel = AdminPanel.objects.filter(uuid=pid).first()
  users = panel.users
  for user in users:
    user_data = UserAuth.objects.filter(uuid=user).first()
    users[user]["email"] = user_data.email
  return users


def get_client_list(pid=None, pObj=None):
  if pid is not None:
    panel = AdminPanel.objects.filter(uuid=pid).first()
  elif pObj is not None:
    panel = pObj
  else:
    return None

  primary_client = panel.primaryClient
  secondary_clients = panel.secondaryClients

  if ',' in secondary_clients:
    secondary_clients = secondary_clients.split(',')
  elif secondary_clients == '' or primary_client == '':
    secondary_clients = ['--- no client ---']
  else:
    secondary_clients = [ secondary_clients, ]

  return [primary_client, ] + secondary_clients


def get_panel_data(pid):
  panel = AdminPanel.objects.filter(uuid=pid).first()
  clients = get_client_list(pObj=panel)
  return {
    "id": panel.uuid,
    "name": panel.name,
    "api": panel.api,
    "apiKey": panel.api_key,
    "primaryClient": clients[0],
    "secondaryClients": clients[1:],
    "image": '/static/eastercompany/favicon.ico',
    "users": panel.users,
    "createCMD": panel.create_cmd,
    "installCMD": panel.install_cmd,
    "runCMD": panel.run_cmd,
    "description": panel.description,
    "isNative": False,
    "isWeb": True
  }


def create_new_panel(uuid, name, api):
  user = UserAuth.objects.filter(uuid=uuid).first()
  new_panel_id = uuid1()
  user.panels = f"{user.panels}{new_panel_id},"
  user.save()
  return AdminPanel.objects.create(
    uuid=new_panel_id,
    name=name,
    api=api,
    users={
      f"{user}": {
        "permissions": 99
      }
    }
  )


def update_application_client_context(pid):
  panel = AdminPanel.objects.filter(uuid=pid).first()
  api_url = get_api_url(panel) + f"panel/view/clients?api_key={panel.api_key}"
  response = requests.get(api_url)
  json_resp = json.loads(response.text)
  panel.primaryClient = json_resp["primaryClient"]
  panel.secondaryClients = json_resp["secondaryClients"]
  panel.save()


def update_application_name_setting(pid, new_domain):
  panel = AdminPanel.objects.filter(uuid=pid).first()
  panel.name = new_domain
  panel.save()


def update_application_api_setting(pid, new_api):
  panel = AdminPanel.objects.filter(uuid=pid).first()
  panel.api = new_api
  panel.save()


def update_application_index_setting(pid, new_index):
  panel = AdminPanel.objects.filter(uuid=pid).first()
  panel.index = new_index
  panel.save()


def update_application_public_key_setting(panel):
  panel 


def update_setting(req, pid, permissions_required, _func):
  panel_id = get_arg(pid)
  user = get_user(req)
  body = get_body(req)
  permissions = get_panel_users(panel_id)[user[0]]["permissions"]
  if permissions >= permissions_required:
    return if_authorized(req, lambda: _func(panel_id, body))
  return error()
