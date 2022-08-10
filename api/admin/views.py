# Standard library
from urllib import parse
# Overlord library
from core.library import api
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


def create(req, uuid, app_name, api_url, *args, **kwargs):
  try:
    user = parse.unquote(uuid).strip()
    name = parse.unquote(app_name).strip()
    url = parse.unquote(api_url).strip()
    create_new_panel(uuid=user, name=name, url=url)
    return api.success()
  except Exception as exception:
    return api.error(exception)
