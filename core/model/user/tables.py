# Overlord library
from email.policy import default
from . import session
from core.library import time, models, uuid, \
  api, encrypt, get_datetime_string, json


class newUserObj:
  auth = None
  details = None
  invites = None


class UserModel(models.Model):
  """
  Inheritor class for user related models, contains the uuid primary key for joining user tables.

  [uuid] 32 hex digits divided into sections separated by 4 dashes totalling 36 characters
      +   formatted in this layout 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
  """
  uuid = models.CharField(
      null=False,
      blank=False,
      unique=True,
      default=uuid,
      max_length=36,
      primary_key=True
  )

  class Meta:
    abstract = True

  def __str__(self):
    """
    Return the selected users uuid as a string

    :return str: uuid
    """
    return str(self.uuid)


class UserDetails(UserModel):
  """
  Contains general non-technical information about the user
  """
  names = models.TextField(default="")
  display_name = models.TextField(default="")
  display_image = models.URLField(default="https://www.easter.company/static/eastercompany/favicon.ico")
  date_of_birth = models.DateTimeField(null=False, blank=False, default=time.get_datetime_string)
  date_joined = models.DateTimeField(null=False, blank=False, default=time.get_datetime_string)


class UserInvite(models.Model):
  """
  This model contains the structure for user invites which allow a user to
  accept an invite to create their account based on a given email or sms
  verification method.
  """
  uuid = models.CharField(
    null=False,
    blank=False,
    unique=True,
    default=uuid,
    max_length=36,
    primary_key=True
  )
  data = models.JSONField(default=None)
  email = models.EmailField(default="")
  sms = models.TextField(default="")
  sent = models.BooleanField(default=False)
  created_by = models.CharField(
    null=False,
    blank=False,
    max_length=36
  )
  created_on = models.DateTimeField(
    null=False,
    blank=False,
    default=get_datetime_string
  )

  @staticmethod
  def create(email="", sms="", data=None):
    UserInvite.objects.create(email=email, sms=sms, data=data)
    return api.success()


class Users(UserModel):
  """
  Contains information to login and maintain a session with the session and
  a new user session is generated upon each login or registration request.
  """
  email = models.TextField(unique=True)
  sms = models.TextField(unique=True)
  key = models.TextField(null=False, blank=False)
  permissions = models.IntegerField(null=False, blank=False, default=0)
  session = models.TextField(unique=True)
  last_activity = models.DateTimeField(default=time.get_datetime_string)
  panels = models.TextField(default="")       # comma separated panel uuid list

  @staticmethod
  def create(email, password, permissions):
    Users.objects.create(
      email=email,
      key=encrypt(password),
      permissions=int(permissions),
      session=session.generate()
    )
    UserDetails.objects.create(
      uuid=uuid,
      display_name=email.split('@')[0] if '@' in email else email
    )
    return api.success()

  @staticmethod
  def deleteAll(uuid):
    """
    Not what it says it the tin; Users.deleteAll() does not delete all users.
    It deletes all records on all tables on all databases related to a single
    user uuid.

    :param uuid str: the user uuid to be totally purged from existence
    :return api.success: None
    """
    user = Users.fetchAll(uuid)
    user.auth.delete()
    user.details.delete()
    for invite in user.invites:invite.delete()
    return api.success()

  @staticmethod
  def fetchAll(uuid):
    user = newUserObj()
    user.auth = Users.fetch(uuid=uuid)
    user.details = UserDetails.objects.filter(uuid=uuid).first()
    user.invites = UserInvite.objects.filter(created_by=uuid)
    return user

  @staticmethod
  def fetch(uuid):
    return Users.objects.filter(uuid=uuid).first()

  def __str__(self, *args, **kwargs):
    user = self.fetchAll(self.uuid)
    return api.data({
      "sms": user.auth.sms,
      "email": user.auth.email,
      "panels": user.auth.panels,
      "permissions": user.auth.permissions,
      "details": {
        "names": user.details.names,
        "display_name": user.details.display_name,
        "display_image": user.details.display_image,
        "date_of_birth": user.details.date_of_birth,
        "date_joined": user.details.date_joined
      },
      "invites": [{
        "email": invite.email,
        "sms": invite.sms,
        "data": invite.data,
        "created_on": invite.created_on
      } for invite in user.invites]
    })
