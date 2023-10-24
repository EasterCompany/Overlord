from .utils import session
from PIL import Image
from io import BytesIO
from datetime import timedelta, timezone
from shared.library import (
  time, models, uuid, settings,
  api, encrypt, decrypt,
  exists, mkdir, remove, rmtree,
  DatabaseError, IntegrityError,
  PILImage, ImageFile, ImageFileError,
)


class UserModel(models.Model):
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


class Users(UserModel):
  email = models.TextField(unique=True)
  key = models.TextField(null=False, blank=False)
  session = models.TextField(unique=True)
  groups = models.JSONField(default=dict)
  permissions = models.IntegerField(null=False, blank=False, default=0)
  first_name = models.TextField(default="")
  middle_names = models.TextField(default="")
  last_name = models.TextField(default="")
  display_name = models.TextField(default="")
  display_image = models.ImageField()
  date_of_birth = models.DateTimeField(blank=False, null=False)
  date_joined = models.DateTimeField(blank=False, default=time.now)
  last_active = models.DateTimeField(default=time.now)

  @staticmethod
  def create(
    email:str,
    password:str,
    first_name:str,
    last_name:str,
    date_of_birth,
    permissions:int=1
  ):
    ''' Creates a new user account '''
    try:
      # Verify Email
      email = email.lower()
      if not len(email) >= 5 or not '@' in email or not '.' in email:
        return api.fail("Must use a valid email address.")
      # Verify Password Criteria
      if not len(password) >= 8:
        return api.fail("Password must be at least 8 characters.")
      # Verify First Name
      if not len(first_name) >= 1:
        return api.fail("Must enter a valid first name.")
      # Verify Last Name
      if not len(last_name) >= 1:
        return api.fail("Must enter a valid last name.")
      # Verify Date of Birth
      date_of_birth = time._datetime.strptime(date_of_birth, "%d/%m/%Y")
      if date_of_birth > time._datetime.now() - timedelta(days=365*13):
        return api.fail("You must be at least 13 years old.")
      date_of_birth = date_of_birth.replace(tzinfo=timezone.utc)
      # Create User
      Users.objects.create(
        email=email,
        key=encrypt(password),
        session=session.generate(),
        permissions=int(permissions),
        first_name=first_name.title(),
        last_name=last_name.title(),
        display_name=email.split('@')[0].title() if '@' in email else email,
        date_of_birth=date_of_birth,
      )
    except IntegrityError as error:
      if str(error) == "UNIQUE constraint failed: core_users.email":
        return api.fail("Email address is already registered.")
      return api.error(error)
    except DatabaseError as error:
      return api.error(error)
    return User(email).json(True)

  @staticmethod
  def login(email:str, password:str):
    ''' Login a user using an email & password combination '''
    try:
      email = email.strip().lower()
      user = User(email)
      if user.data is not None and password == user.password:
        return user.json(True)
      return api.fail("Invalid email & password combination.")
    except Exception as exception:
      return api.error(exception)

  @staticmethod
  def refresh(uuid:str, session:str):
    ''' Resync the user data stored on the local device '''
    try:
      user = User(uuid)
      if session == user.data.session:
        return user.json(True)
      return api.error()
    except Exception as exception:
      return api.error(exception)

  @staticmethod
  def purge(uuid:str, password:str):
    ''' Deletes all records related to an existing uuid '''
    try:
      user = User(uuid)
      if not password == user.password:
        return api.std(api.BAD, "Invalid password.")
      user.delete()
      return api.success()
    except Exception as exception:
      return api.error(exception)

  @staticmethod
  def change_email(uuid:str, new_email:str, password:str):
    ''' Update the email of an existing user based on uuid. '''
    try:
      # Verify New Email
      if not len(new_email) >= 5 or not '@' in new_email or not '.' in new_email:
        return api.fail("Must use a valid email address.")

      user = User(uuid)
      if password == user.password:
        try:
          user.data.email = new_email.strip().lower()
          user.data.save()
        except Exception:
          return api.fail("Encountered an error, email might already be registered.")
        return user.json(True)
      else:
        return api.fail("Invalid password.")

    except Exception as exception:
      return api.error(exception)

  @staticmethod
  def change_password(uuid:str, current_password:str, new_password:str, confirm_password:str):
    ''' Update the password of an existing user based on uuid. '''
    try:
      if not len(new_password) >= 8:
        return api.fail("Password must be at least 8 characters.")
      if not new_password == confirm_password:
        return api.fail("Passwords do not match.")

      user = User(uuid)
      if not current_password == user.password:
        return api.fail("Invalid current password.")

      user.data.key = encrypt(new_password)
      user.data.save()
      return user.json(True)
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
      if session != user.data.session:
        return api.fail("Failed authentication, try logging out and then back in.")

      if first_name is not None:
        if len(first_name) == 0:
          return api.fail('User must have a first name.')
        user.data.first_name = first_name
      if middle_names is not None:
        user.data.middle_names = middle_names
      if last_name is not None:
        if len(last_name) == 0:
          return api.fail('User must have a last name.')
        user.data.last_name = last_name
      if display_image is not None:
        file_name, file_content = api.get_decoded_base64_file("display_image", display_image)
        if user.create_file(name=file_name, content=file_content, resize=(132, 132)):
          user.data.display_image.delete()
          user.data.display_image = f"{user.data.uuid}/{file_name}"

      user.data.save()
      return user.json(True)
    except Exception as exception:
      return api.error(exception)


class User:

  def __init__(self, identifier:str, no_decrypt=False, *args, **kwargs) -> None:
    if '@' in identifier:
      self.data = Users.objects.filter(email=identifier).first()
    else:
      self.data = Users.objects.filter(uuid=identifier).first()
    if self.data is not None:
      self.password = self.data.key if no_decrypt else decrypt(self.data.key)
      self.invites = UserInvite.objects.filter(created_by=self.data.uuid)
      self.content_dir = f"{settings.MEDIA_DIR}/{self.data.uuid}"

  def delete(self) -> None:
    self.data.delete()
    if self.invites.count() > 0:
      self.invites.delete()
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

  def json(self, include_private_data=False) -> dict:
    return api.data({
      "uuid": self.data.uuid,
      "session": self.data.session if include_private_data else None,
      "email": self.data.email,
      "groups": self.data.groups,
      "permissions": self.data.permissions,
      "firstName": self.data.first_name,
      "middleNames": self.data.middle_names,
      "lastName": self.data.last_name,
      "displayName": self.data.display_name,
      "displayImage": f"/static{self.data.display_image.url}" if self.data.display_image else "",
      "dateOfBirth": time.timestamp(self.data.date_of_birth, False, True),
      "dateJoined": time.timestamp(self.data.date_joined, False, True),
      "lastActive": time.timestamp(self.data.last_active, True, True),
      "invites": [{
        "email": invite.email,
        "data": invite.data,
        "created_on": time.timestamp(invite.created_on, False, True)
      } for invite in self.invites]
    })
