# Overlord library
import re
from core.library.api import get_arg
from api.user.controls import if_authorized
from api.admin.controls import *


def view_user(req, uuid, *args, **kwargs):
  """
  Returns a list of all the panels that a specific user has access to

  :param uuid str: user identifier
  :return api data:
  """
  user_id = get_arg(uuid)
  return if_authorized(req, lambda: get_user_panels(user_id))


def view_panel(req, pid, *args, **kwargs):
  """
  Returns a dictionary containing all the data associated with a specific panel

  :param pid str: panel identifier
  :return api data: { uuid: <str>, name: <str>, url: <str>, users: {...} }
  """
  panel_id = get_arg(pid)
  return if_authorized(req, lambda: get_panel_data(panel_id))


def view_panel_users(req, pid, *args, **kwargs):
  """
  Returns a dictionary containing all the users associated with a specific panel

  :param pid str: panel identifier
  :return api data: { uuid: { email: <str>, permissions: <int> } ... }
  """
  panel_id = get_arg(pid)
  return if_authorized(req, lambda: get_panel_users(panel_id))


def create(req, uuid, app_name, api_url, *args, **kwargs):
  """
  Creates a panel in the database which the user can login to and begin modifying

  :param uuid: user identifier
  :param app_name: what the panel will also be named
  :param api_url: where the panel will communicate with the app
  :return api status:
  """
  user_id = get_arg(uuid)
  panel_name = get_arg(app_name)
  panel_api_url = get_arg(api_url)
  return if_authorized(req, lambda: create_new_panel(uuid=user_id, name=panel_name, url=panel_api_url))


def verify_user(req, pid, uuid, *args, **kwargs):
  """
  Returns a users permission level as a response when verifying their identity

  :param pid str: panel identifier
  :param uuid str: user identifier
  :return api data: { permissions: <int> }
  """
  panel_id = get_arg(pid)
  user_id = get_arg(uuid)
  return if_authorized(req, lambda: get_panel_users(panel_id)[user_id])
