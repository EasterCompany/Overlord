# Standard library
from uuid import uuid1
# Overlord library
from api.user.tables import UserAuth
from api.admin.tables import AdminPanel


def get_user_panels(uuid):
  user = UserAuth.objects.filter(uuid=uuid).first()
  if ',' in user.panels:
    return user.panels.split(',')[:-1]
  return []


def get_panel_users(uuid):
  panel = AdminPanel.objects.filter(uuid=uuid).first()
  return panel.users


def get_panel_data(uuid):
  panel = AdminPanel.objects.filter(uuid=uuid).first()
  return {
    "name": panel.app_name,
    "api": panel.api_url,
    "image": '/static/eastercompany/favicon.ico',
    "users": panel.users
  }


def create_new_panel(uuid, name, url):
  user = UserAuth.objects.filter(uuid=uuid).first()
  new_panel_id = uuid1()
  user.panels = f"{user.panels}{new_panel_id},"
  user.save()
  return AdminPanel.objects.create(
    uuid=new_panel_id,
    app_name=name,
    api_url=url,
    users={
      f"{user}": {
        "permissions": 99
      }
    }
  )
