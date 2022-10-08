# Overlord library
from os import stat
from . import session
from core.library import time, models, uuid, \
  api, encrypt, get_datetime_string, json, JsonResponse


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
  sms = models.TextField(null=False, blank=False, default="")
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
      uuid=Users.objects.filter(email=email).first().uuid,
      display_name=email.split('@')[0] if '@' in email else email
    )
    return api.success()

  @staticmethod
  def purge(uuid):
    Users.objects.filter(uuid=uuid).delete()
    UserDetails.objects.filter(uuid=uuid).delete()
    UserInvite.objects.filter(created_by=uuid).delete()
    return api.success()

  @staticmethod
  def _fetchAll(uuid):
    user = newUserObj()
    user.auth = Users.objects.filter(uuid=uuid).first()
    user.details = UserDetails.objects.filter(uuid=uuid).first()
    user.invites = UserInvite.objects.filter(created_by=uuid)
    return user

  @staticmethod
  def fetch(uuid):
    user = Users._fetchAll(uuid)
    return {
      "uuid": user.auth.uuid,
      "sms": user.auth.sms,
      "email": user.auth.email,
      "panels": user.auth.panels,
      "permissions": user.auth.permissions,
      "details": {
        "names": user.details.names,
        "display_name": user.details.display_name,
        "display_image": user.details.display_image,
        "date_of_birth": str(user.details.date_of_birth),
        "date_joined": str(user.details.date_joined)
      },
      "invites": [{
        "email": invite.email,
        "sms": invite.sms,
        "data": invite.data,
        "created_on": str(invite.created_on)
      } for invite in user.invites]
    }

  @staticmethod
  def fetchAll():
    pass

  @staticmethod
  def view(uuid):
    return JsonResponse(Users.fetch(uuid))

  @staticmethod
  def list(uuid):
    return JsonResponse(Users.fetchAll())
