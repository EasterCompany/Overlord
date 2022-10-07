# Overlord library
from . import API
from core.models import Users
from core.library import unquote, json

API.path(
    "view",
    lambda req, *args, **kwargs: Users.list(),
    "List All Users"
)

API.path(
    "view/<str:uuid>",
    lambda req, uuid, *args, **kwargs: Users.view(uuid),
    "View User By ID"
)

API.path(
    "create/<str:email>/<str:permissions>",
    lambda req, email, permissions, *args, **kwargs: Users.create(
        unquote(email), req.body.decode('utf-8'), unquote(permissions)
    ),
    "Create New User"
)

API.path(
    "edit/<str:uuid>",
    lambda req, uuid, *args, **kwargs: Users.edit(uuid, json.loads(req.body.decode('utf-8'))),
    "Edit Existing User Data"
)

API.path(
    "delete/<str:uuid>",
    lambda req, uuid, *args, **kwargs: Users.deleteAll(uuid=uuid),
    "Delete User by UUID"
)

API.path(
    "login/<str:email>",
    lambda req, email, *args, **kwargs: Users.login(email=unquote(email), password=req.body.decode('utf-8')),
    "Login User by Email"
)

API.path(
    "login/<str:sms>",
    lambda req, sms, *args, **kwargs: Users.login(sms=unquote(sms), password=req.body.decode('utf-8')),
    "Login User by SMS"
)
