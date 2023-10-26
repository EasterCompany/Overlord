from shared import api, settings
from .apps import
from user.models import Users

API.path(
  "create",
  lambda req, *args, **kwargs: Users.create(**api.get_json(req)),
  "Create New User"
)

API.path(
  "login",
  lambda req, *args, **kwargs: Users.login(**api.get_json(req)),
  "Returns session data for an email/password combination"
)

API.path(
  "refresh",
  lambda req, *args, **kwargs: Users.refresh(**api.get_json(req)),
  "Returns session data for an uuid/session combination"
)

API.path(
  "delete",
  lambda req, *args, **kwargs: Users.purge(**api.get_json(req)),
  "Deletes all user data related to a specific uuid"
)

API.path(
  "edit/email",
  lambda req, *args, **kwargs: Users.change_email(**api.get_json(req)),
  "Updates the users email to a new one"
)

API.path(
  "edit/password",
  lambda req, *args, **kwargs: Users.change_password(**api.get_json(req)),
  "Verifies the current user password and updates it to a new one"
)

API.path(
  "edit/details",
  lambda req, *args, **kwargs: Users.change_details(**api.get_json(req)),
  "Updates the users details"
)

# Export URLS & Sockets
urlpatterns = [
  API.urls,
]
if not settings.DEBUG and not :
  urlpatterns.append(
    (
      r'^ws/(?P<path>.*)$',
      'django.contrib.staticfiles.urls.staticfiles_url',
      {'document_root': STATIC_FILES}
    ),
  )
