# Overlord library
from core.models import Users
from core.library import api


def authorized(uuid, sesh):
  return Users.objects.filter(uuid=uuid).only()[0].session.split("[:~OLT~:]")[1] == sesh


def if_authorized(req, do_function):
  try:
    auth_uuid, auth_sesh = api.get_user(req)
    if authorized(auth_uuid, auth_sesh):
      r = do_function()
      if isinstance(r, bool):
        return api.success() if r is True else api.error()
      elif isinstance(r, dict) or isinstance(r, list) or \
          isinstance(r, int) or isinstance(r, float) or \
          isinstance(r, str): return api.data(r)
      return api.success()
    return api.error("Unauthorized access.")
  except Exception as exception:
    return api.error(exception)
