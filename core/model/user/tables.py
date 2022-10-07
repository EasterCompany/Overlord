# Overlord library
from . import session
from core.library import time, models, uuid, get_datetime_string, api, encrypt


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
  first_name = models.TextField(default="")
  middle_names = models.TextField(default="")
  last_name = models.TextField(default="")
  display_image = models.TextField(default="")
  display_name = models.TextField(null=True, blank=True, default="")
  date_of_birth = models.DateField(null=False, blank=False)
  date_joined = models.DateField(null=False, blank=False, default=time.get_datetime_string)

  @staticmethod
  def create(email, password, permissions):
    return UserAuth.create(email, password, permissions)

  @staticmethod
  def delete(req, uuid, *args, **kwargs):
    return UserAuth.delete(uuid)


class UserAuth(UserModel):
  """
  Contains information to login and maintain a session with the session and
  a new user session is generated upon each login or registration request.
  """
  email = models.TextField(null=False, blank=False, unique=True)
  sms = models.TextField(unique=True, null=True, blank=True)
  key = models.TextField(null=False, blank=False)
  authenticated_email = models.BooleanField(default=False)
  authenticated_sms = models.BooleanField(default=False)
  permissions = models.IntegerField(null=True, blank=True)
  session = models.TextField(null=False, blank=False, unique=True)
  last_activity = models.DateTimeField(null=False, blank=False, default=time.get_datetime_string)
  active = models.BooleanField(null=False, blank=False, default=False)
  panels = models.TextField(null=False, blank=False, default="")

  @staticmethod
  def create(email, password, permissions):
    # Check if email already exists
    if UserAuth.objects.filter(email=email).count() > 0:
      return api.std(message="Email already exists", status=api.BAD)
    # Encrypt password
    encrypted_password = encrypt(password)
    # Create new user
    UserAuth.objects.create(
      email=email,
      key=encrypted_password,
      permissions=int(permissions),
      session=session.generate()
    )
    return api.success()

  @staticmethod
  def delete(req, uuid, *args, **kwargs):
    obj = UserAuth.objects.filter(uuid=uuid)

    if obj.count() <= 0:
      return api.error(
        "    When trying to delete a user,\n    no `UserAuth Table` db record matching UUID"
        f"\n     {uuid}\n     was found."
      )

    try:
      obj = obj.first()
      obj.delete()
    except Exception as exception:
      return api.error(exception)

    try:
      obj = UserDetails.objects.filter(uuid=uuid).first()
      obj.delete()
    except Exception as exception:
      return api.error(exception)

    return api.std(message="success", status=api.OK)


class UserInvite(models.Model):
  """
  This model contains the structure for user invites which allow a user to
  accept an invite to create their account based on a given email or sms
  verification method.
  """
  # Primary Key
  uuid = models.CharField(
    null=False,
    blank=False,
    unique=True,
    default=uuid,
    max_length=36,
    primary_key=True
  )
  # Invite data
  data = models.JSONField()
  email = models.EmailField(default="")
  sms = models.TextField(default="")
  sent = models.BooleanField(default=False)
  # Foreign UUID
  created_by = models.CharField(
    null=False,
    blank=False,
    max_length=36
  )
  # Datetime Object
  created_on = models.DateTimeField(
    null=False,
    blank=False,
    default=get_datetime_string
  )

  @staticmethod
  def create(email="", sms="", data=None):
    UserInvite.objects.create(email=email, sms=sms, data=data)
    return api.success()
