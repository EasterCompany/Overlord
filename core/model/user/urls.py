# Overlord library
from . import API
from core.library import unquote, json
from core.model.user.tables import UserAuth as User

API.path(
    API("view"),
    lambda req, *args, **kwargs: User.list(),
    name="List All Users"
)

API.path(
    API("view/<str:uuid>"),
    lambda req, uuid, *args, **kwargs: User.view(uuid),
    name="View User By ID"
)

API.path(
    API("create/<str:email>/<str:permissions>"),
    lambda req, email, permissions, *args, **kwargs: User.create(
        unquote(email), req.body.decode('utf-8'), unquote(permissions)
    ),
    name="Create New User"
)

API.path(
    API("edit/<str:uuid>"),
    lambda req, uuid, *args, **kwargs: User.edit(uuid, json.loads(req.body.decode('utf-8'))),
    name="Edit Existing User Data"
)

API.path(
    API("delete/<str:uuid>"),
    lambda req, uuid, *args, **kwargs: User.delete(uuid),
    name="Delete User by UUID"
)

API.path(
    API("login/<str:email>"),
    lambda req, email, *args, **kwargs: User.email_login(unquote(email), req.body.decode('utf-8')),
    name="Login User by Email"
)

API.path(
    API("login/<str:sms>"),
    lambda req, sms, *args, **kwargs: User.sms_login(unquote(sms), req.body.decode('utf-8')),
    name="Login User by SMS"
)
