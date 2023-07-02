# Overlord library
from . import session
from PIL import Image
from io import BytesIO
from datetime import timedelta, timezone
from web.settings import SERVER_DATA
from core.library import (
  time, models, uuid,
  api, encrypt, decrypt,
  exists, mkdir, remove, rmtree,
  DatabaseError, IntegrityError
)


class UserModel(models.Model):
  """
  Inheritor class for user related models, contains the uuid primary key used for joining tables.
  The uuid is a 32 hex digit string divided into 5 sections separated by 4 dashes totalling 36
  characters which look like this:

  'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'

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
    ''' Returns the users uuid when converted to a string '''
    return str(self.uuid)


class UserInvite(models.Model):
  '''
  This model contains the structure for user invites which allows a user to
  accept an invite and create an account using a specified email address
  '''
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
  ''' Contains general non-technical information about the user '''
  first_name = models.TextField(default="")
  middle_names = models.TextField(default="")
  last_name = models.TextField(default="")
  display_name = models.TextField(default="")
  display_image = models.ImageField()
  date_of_birth = models.DateTimeField(blank=False, default=time._datetime.now)
  date_joined = models.DateTimeField(blank=False, default=time._datetime.now)


class Users(UserModel):
  ''' Core database model for user authentication & management '''
  email = models.TextField(unique=True)
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
    ''' Creates a new user with the minimum requirements '''
    try:
      # Verify Email Criteria
      email = email.lower()
      if not len(email) >= 5 or not '@' in email or not '.' in email:
        return api.std(api.BAD, "Must use a valid email address.")

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

    except IntegrityError as error:
      if str(error) == "UNIQUE constraint failed: core_users.email":
        return api.std(api.BAD, "Email address is already registered.")
      return api.error(error)

    except DatabaseError as error:
      return api.error(error)

    return api.success()

  @staticmethod
  def login(email:str, password:str):
    ''' Login a user using an email & password combination '''
    try:
      user = Users.fetch(identifier=email.lower(), include_private_data=True)
      if password == decrypt(user['key']):
        return api.data(user)
      return api.std(api.BAD, "Invalid email & password combination.")
    except Exception as exception:
      return api.error(exception)

  @staticmethod
  def refresh(uuid:str, session:str):
    ''' Resync the user data stored on the local device '''
    try:
      user = Users.fetch(identifier=uuid, include_private_data=True)
      if session == user['session']:
        return api.data(user)
      return api.error()
    except Exception as exception:
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
      "email": user.auth.email,
      "permissions": user.auth.permissions,
      "firstName": user.details.first_name,
      "middleNames": user.details.middle_names,
      "lastName": user.details.last_name,
      "displayName": user.details.display_name,
      "displayImage": f"/static{user.details.display_image.url}" if user.details.display_image else "",
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
  def delete(uuid:str = "", password:str = ""):
    ''' Delete all records related to an existing uuid '''
    try:
      user = User(uuid)
      if not password == decrypt(user.auth.key):
        return api.std(api.BAD, "Invalid password.")
      user.delete()
      return api.success()
    except Exception as exception:
      return api.error(exception)

  @staticmethod
  def change_email(uuid:str, new_email:str, password:str):
    ''' Update the email of an existing user based on uuid. '''
    try:
      user = User(uuid)
      if password == decrypt(user.auth.key):
        try:
          user.auth.email = new_email
          user.auth.save()
        except Exception:
          return api.std(api.BAD, "Encountered an error, email might already be registered.")
        return api.success()
      else:
        return api.std(api.BAD, "Invalid password.")
    except Exception as exception:
      return api.error(exception)

  @staticmethod
  def change_password(uuid:str, current_password:str, new_password:str, confirm_password:str):
    ''' Update the password of an existing user based on uuid. '''
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

  @staticmethod
  def change_details(
    uuid:str,
    session: str,
    first_name:str|None = None,
    middle_names:str|None = None,
    last_name:str|None = None,
    display_image:str|None = None
  ):
    ''' Update the display image for an existing user based on uuid. '''
    try:
      user = User(uuid)
      if user.auth.session != session:
        return api.error()

      if first_name is not None:
        user.details.first_name = first_name
      if middle_names is not None:
        user.details.middle_names = middle_names
      if last_name is not None:
        user.details.last_name = last_name
      if display_image is not None:
        file_name, file_content = api.get_decoded_base64_file("di", display_image)
        if user.create_file(name=file_name, content=file_content, resize=(132, 132)):
          user.details.display_image.delete()
          user.details.display_image = f"{user.auth.uuid}/{file_name}"

      user.details.save()
      return api.data(Users.fetch(user.auth.uuid, include_private_data=True))
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
    self.content_dir = f"{SERVER_DATA['MEDIA_DIR']}/{self.auth.uuid}"

  def delete(self) -> None:
    Users.objects.filter(uuid=self.auth.uuid).delete()
    UserDetails.objects.filter(uuid=self.auth.uuid).delete()
    invites = UserInvite.objects.filter(created_by=self.auth.uuid)
    if invites.count() > 0:
      invites.delete()
    if exists(self.content_dir):
      rmtree(self.content_dir)

  def create_file(self, name:str, content:bytes, resize:set|None = None) -> bool:
    file_path = f"{self.content_dir}/{name}"
    if not exists(self.content_dir):
      mkdir(self.content_dir)
    if exists(file_path):
      remove(file_path)
    if resize is not None:
      content = Image.open(BytesIO(content)).resize(resize).save(file_path)
    else:
      with open(file_path, "+wb") as new_file:
        new_file.write(content)
    return exists(file_path)
