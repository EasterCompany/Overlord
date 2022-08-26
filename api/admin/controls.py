# Standard library
from uuid import uuid1
# Overlord library
from api.user.tables import UserAuth
from api.user.controls import if_authorized
from api.admin.tables import AdminPanel
from core.library.api import get_arg, get_user, get_body, error


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


def get_panel_data(pid):
  panel = AdminPanel.objects.filter(uuid=pid).first()
  return {
    "id": panel.uuid,
    "name": panel.name,
    "api": panel.api,
    "index": 'e_panel',
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


def update_application_name_setting(pid, new_domain):
  panel = AdminPanel.objects.filter(uuid=pid).first()
  panel.name = new_domain
  panel.save()
  print(panel.name)


def update_application_api_setting(pid, new_api):
  panel = AdminPanel.objects.filter(uuid=pid).first()
  panel.api = new_api
  panel.save()


def update_setting(req, pid, permissions_required, _func):
  panel_id = get_arg(pid)
  user = get_user(req)
  body = get_body(req)
  permissions = get_panel_users(panel_id)[user[0]]["permissions"]
  if permissions >= permissions_required:
    return if_authorized(req, lambda: _func(panel_id, body))
  return error()
