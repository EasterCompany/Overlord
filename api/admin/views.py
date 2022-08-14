# Standard library
from urllib import parse
# Overlord library
from core.library import api
from api.user.controls import if_authorized
from api.admin.controls import *


def view_user(req, uuid, *args, **kwargs):
  try:
    user = parse.unquote(uuid).strip()
    user_panels = get_user_panels(user)
    return api.data(user_panels)
  except Exception as exception:
    return api.error(exception)


def view_panel(req, uuid, *args, **kwargs):
  try:
    panel = parse.unquote(uuid).strip()
    panel_data = get_panel_data(panel)
    return api.data(panel_data)
  except Exception as exception:
    return api.error(exception)


def view_panel_users(req, uuid, *args, **kwargs):
  try:
    panel = parse.unquote(uuid).strip()
    panel_data = get_panel_users(panel)
    return api.data(panel_data)
  except Exception as exception:
    return api.error(exception)


def create(req, uuid, app_name, api_url, *args, **kwargs):
  user = parse.unquote(uuid).strip()
  name = parse.unquote(app_name).strip()
  url = parse.unquote(api_url).strip()
  return if_authorized(req, uuid, lambda: create_new_panel(uuid=user, name=name, url=url))
  try:
    create_new_panel(uuid=user, name=name, url=url)
    return api.success()
  except Exception as exception:
    return api.error(exception)


def verify_user(req, pid, uuid, *args, **kwargs):
  return if_authorized(req, uuid, lambda: get_panel_users(pid)[uuid])
  try:
    users = get_panel_users(pid)
    if uuid in users and authorize(req, uuid):
      user_permissions = users[uuid]
      return api.data(user_permissions)
    return api.error()
  except Exception as exception:
    return api.error(exception)
