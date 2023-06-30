# Overlord library
from . import session
from datetime import timedelta, timezone
from django.db import DatabaseError, IntegrityError
from core.library import time, models, uuid, api, encrypt, decrypt, console


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

  def __str__(self, *args, **kwargs):
    """
    Return the selected users uuid as a string

    :return str: uuid
    """
    return str(self.uuid)


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
    default=time._datetime.now
  )

  @staticmethod
  def fetch(email):
    return UserInvite.objects.filter(email=email)


class UserDetails(UserModel):
  """
  Contains general non-technical information about the user
  """
  first_name = models.TextField(default="")
  middle_names = models.TextField(default="")
  last_name = models.TextField(default="")
  display_name = models.TextField(default="")
  display_image = models.URLField(default="")
  date_of_birth = models.DateTimeField(blank=False, default=time._datetime.now)
  date_joined = models.DateTimeField(blank=False, default=time._datetime.now)


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
  last_active = models.DateTimeField(default=time._datetime.now)

  @staticmethod
  def create(
    email:str,
    password:str,
    first_name:str,
    last_name:str,
    date_of_birth,
    permissions:int=1
  ):
    try:
      # Verify Email Criteria
      email = email.lower()
      if not len(email) >= 5 or not '@' in email or not '.' in email:
        return api.std(api.BAD, "Must use a valid email address")

      # Verify Password Criteria
      if not len(password) >= 8:
        return api.std(api.BAD, "Password must be at least 8 characters.")

      # Verify Date of Birth
      date_of_birth = time._datetime.strptime(date_of_birth, "%d/%m/%Y")
      if date_of_birth > time._datetime.now() - timedelta(days=365*13):
        return api.std(api.BAD, "You must be at least 13 years old.")
      date_of_birth = date_of_birth.replace(tzinfo=timezone.utc)

      # Create User
      Users.objects.create(
        email=email,
        key=encrypt(password),
        permissions=int(permissions),
        session=session.generate()
      )
      UserDetails.objects.create(
        uuid=Users.objects.get(email=email).uuid,
        first_name=first_name.title(),
        last_name=last_name.title(),
        date_of_birth=date_of_birth,
        display_name=email.split('@')[0].title() if '@' in email else email
      )
      console.log(f"New user created with email {email} and permission level of {permissions}")

    except IntegrityError as error:
      if str(error) == "UNIQUE constraint failed: core_users.email":
        return api.std(api.BAD, "Email address is already registered.")
      return api.error(error)

    except DatabaseError as error:
      return api.error(error)

    return api.success()

  @staticmethod
  def login(email:str, password:str):
    '''
    Login a user using a email & password combination
    '''
    try:
      user = Users.fetch(identifier=email.lower(), include_private_data=True)
      if password == decrypt(user['key']):
        return api.data(user)
      print(user)
      return api.error()
    except Exception as exception:
      print(exception, str(exception))
      return api.error(exception)

  @staticmethod
  def fetch(identifier:str, include_private_data=False):
    '''
    Loads all user data related to an identifier into
    a dictionary, usually for returning as a JSON response.
    '''
    try:
      user = User(identifier)
    except Exception as error:
      return error
    return {
      "uuid": user.auth.uuid,
      "key": user.auth.key if include_private_data else None,
      "session": user.auth.session if include_private_data else None,
      "sms": user.auth.sms,
      "email": user.auth.email,
      "permissions": user.auth.permissions,
      "firstName": user.details.first_name,
      "middleNames": user.details.middle_names,
      "lastName": user.details.last_name,
      "displayName": user.details.display_name,
      "displayImage": user.details.display_image,
      "dateOfBirth": time.timestamp(user.details.date_of_birth, False, True),
      "dateJoined": time.timestamp(user.details.date_joined, False, True),
      "lastActive": time.timestamp(user.auth.last_active, True, True),
      "invites": [{
        "email": invite.email,
        "sms": invite.sms,
        "data": invite.data,
        "created_on": str(invite.created_on)
      } for invite in user.invites]
    }

  @staticmethod
  def delete(uuid:str, session:str, password:str):
    '''
    Delete all user data related to a specific uuid.
    requires a session token & password for verification.
    '''
    try:
      DeleteUser(uuid=uuid, session=session, password=password)
      return api.success()
    except Exception as exception:
      return api.error(exception)

  @staticmethod
  def change_email(uuid:str, new_email:str, password:str):
    '''
    Update the email of an existing user based on uuid.
    '''
    try:
      user = User(uuid)
      if password == decrypt(user.auth.key):
        user.auth.email = new_email
        user.auth.save()
        return api.success()
      else:
        return api.std(api.BAD, "Invalid password.")
    except Exception as exception:
      return api.error(exception)

  @staticmethod
  def change_password(uuid:str, current_password:str, new_password:str, confirm_password:str):
    '''
    Update the password of an existing user based on uuid.
    '''
    try:
      if not len(new_password) >= 8:
        return api.error("Password must be at least 8 characters.")
      if not new_password == confirm_password:
        return api.error("Passwords do not match.")
      user = User(uuid)
      if not current_password == decrypt(user.auth.key):
        return api.error("Invalid current password.")
      user.auth.key = encrypt(new_password)
      user.auth.save()
      return api.success()
    except Exception as exception:
      return api.error(exception)


class User:

  def __init__(self, identifier:str, *args, **kwargs) -> None:
    if '@' in identifier:
      self.auth = Users.objects.filter(email=identifier).first()
    else:
      self.auth = Users.objects.filter(uuid=identifier).first()
    self.details = UserDetails.objects.filter(uuid=self.auth.uuid).first()
    self.invites = UserInvite.objects.filter(created_by=self.auth.uuid)


class DeleteUser:

  def __init__(self, uuid:str, session:str, password:str, *args, **kwargs) -> None:
    self.auth = Users.objects.filter(uuid=uuid)
    if session == self.auth.first().session and password == decrypt(self.auth.first().key):
      UserDetails.objects.filter(uuid=self.auth.first().uuid).delete()
      UserInvite.objects.filter(created_by=self.auth.first().uuid).delete()
      self.auth.delete()
