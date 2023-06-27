# Overlord library
from . import API
from core.models import Users
from core.library import unquote, json, api


def _inviteUser(req, *args, **kwargs):
  invite = json.loads(req.body.decode('utf-8'))
  return Users.invite(invite["email"], invite["createdBy"], invite["data"])


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
  "create",
  lambda req, permissions, *args, **kwargs: Users.create(
    api.get_json(req)['email'],
    api.get_json(req)['password']
  ),
  "Create New User"
)

API.path(
  "invite",
  _inviteUser,
  "Invite a New User"
)

API.path(
  "invite/<str:email>",
  lambda req, email, *args, **kwargs: Users.has_invites(email),
  "Check for an Invite"
)

API.path(
  "invite/<str:email>/accept",
  lambda req, email, *args, **kwargs: Users.accept_invite_and_create(api.get_arg(email), api.get_body(req)),
  "Accept an Invite & Create User"
)

API.path(
  "edit/<str:uuid>",
  lambda req, uuid, *args, **kwargs: Users.edit(uuid, json.loads(req.body.decode('utf-8'))),
  "Edit Existing User Data"
)

API.path(
  "delete/<str:uuid>",
  lambda req, uuid, *args, **kwargs: Users.purge(uuid=uuid),
  "Purge all User Data related to specific UUID"
)

API.path(
  "login",
  lambda req, *args, **kwargs: Users.login(req),
  "User Email/Password Login"
)

""" API.path(
  "login/<str:sms>",
  lambda req, sms, *args, **kwargs: Users.login(sms=unquote(sms), password=req.body.decode('utf-8')),
  "Login User by SMS"
) """
