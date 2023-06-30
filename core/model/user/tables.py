# Overlord library
from . import session
from datetime import timedelta, timezone
from django.db import DatabaseError, IntegrityError
from core.library import time, models, uuid, \
  api, encrypt, decrypt, JsonResponse
from core.library import console


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
  def invite(email:str, invited_by:str = "", data:str = ""):
    ''' data contains additional invite information '''
    email = email.lower()                                         # Emails are not case sensitive
    if UserInvite.objects.filter(email=email, data=data).count() == 0 and \
      Users.objects.filter(email=email).count() == 0:
      UserInvite.objects.create(email=email, created_by=invited_by, data=data)
      console.log(f"New invite created for {email} by {invited_by}")
      return api.success()
    return api.error()

  @staticmethod
  def create(
    email:str,
    password:str,
    first_name:str,
    last_name:str,
    date_of_birth,
    permissions:int=1
  ):
    ''' default user permission level is 1 '''
    try:
      email = email.lower()
      date_of_birth = time._datetime.strptime(date_of_birth, "%d/%m/%Y")
      if date_of_birth > time._datetime.now() - timedelta(days=365*13):
        return api.std(api.BAD, "You must be at least 13 years old.")
      date_of_birth = date_of_birth.replace(tzinfo=timezone.utc)

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
  def has_invites(email:str):
    ''' check if an email has invites '''
    invites = UserInvite.fetch(email)
    if invites.count() == 0:
      return api.error()
    return api.success()

  @staticmethod
  def accept_invite_and_create(email:str, password:str):
    ''' accept an invite and create a user '''
    # Get list of invites for this email
    invites = UserInvite.objects.filter(email=email.lower())      # Emails are not case sensitive
    if invites.count() == 0:
      return api.error()
    # Make a list of a panels this email was invited to
    invited_panels = []
    for invite in invites:
      if "ePanelInvite" in invite.data and invite.data["ePanelInvite"] not in invited_panels:
        invited_panels.append(invite.data["ePanelInvite"])
    # Create new user with email
    if Users.objects.filter(email=email).count() == 0:
      Users.create(email, password, 1)
    if len(invited_panels) > 0:
      # Add panels to users panel list
      user = Users.objects.get(email=email)
      user.panels = ','.join(invited_panels) + ','
      user.save()
      for panel in user.panels.split(',')[:-1]:
        try:
          AdminPanel.add_user_to_panel(user.uuid, panel, 1)
        except:
          pass
      invites.delete()
    # Response status
    return api.success()

  @staticmethod
  def get(user:str):
    ''' acquires the user object by uuid or email identifier '''
    if '@' in user:
      try:
        return Users.objects.get(email=user)
      except Exception as error:
        return error
    else:
      try:
        return Users.objects.get(uuid=user)
      except Exception as error:
        return error

  @staticmethod
  def login(email:str, password:str):
    ''' login a user via http request or email/pass parameters '''
    user = Users.fetch(email.lower(), include_private_data=True)
    if isinstance(user, Exception):
      return api.error(user)
    elif password == decrypt(user['key']):
      return api.data(user)
    return api.error()

  @staticmethod
  def purge(uuid):
    Users.objects.filter(uuid=uuid).delete()
    UserDetails.objects.filter(uuid=uuid).delete()
    UserInvite.objects.filter(created_by=uuid).delete()
    console.log(f"User data for {uuid} was purged")
    return api.success()

  @staticmethod
  def _fetchAll(uuid):
    user = newUserObj()
    if '@' in uuid:
      user.auth = Users.objects.filter(email=uuid).first()
    else:
      user.auth = Users.objects.filter(uuid=uuid).first()
    user.details = UserDetails.objects.filter(uuid=user.auth.uuid).first()
    user.invites = UserInvite.objects.filter(created_by=user.auth.uuid)
    return user

  @staticmethod
  def fetch(uuid:str, include_private_data=False):
    try:
      user = Users._fetchAll(uuid)
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
  def fetchAll():
    pass

  @staticmethod
  def view(uuid):
    return JsonResponse(Users.fetch(uuid))

  @staticmethod
  def list():
    return JsonResponse(Users.fetchAll())
