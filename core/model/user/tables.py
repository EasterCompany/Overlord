# Overlord library
from . import session
from core.library import time, models, uuid, \
  api, encrypt, decrypt, get_datetime_string, \
  JsonResponse
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
    default=get_datetime_string
  )

  @staticmethod
  def fetch(email):
    return UserInvite.objects.filter(email=email)


class UserDetails(UserModel):
  """
  Contains general non-technical information about the user
  """
  names = models.TextField(default="")
  display_name = models.TextField(default="")
  display_image = models.URLField(default="https://www.easter.company/static/eastercompany/favicon.ico")
  date_of_birth = models.DateTimeField(null=False, blank=False, default=time.get_datetime_string)
  date_joined = models.DateTimeField(null=False, blank=False, default=time.get_datetime_string)


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
  panels = models.TextField(default="")                           # Comma separated panel uuid list

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
  def create(email:str, password:str, permissions:int=1):
    ''' default user permission level is 1 '''
    email = email.lower()                                         # Emails are not case sensitive
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
    console.log(f"New user created with email {email} and permission level of {permissions}")
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
  def login(req=None, email:str = "", password:str = ""):
    ''' login a user via http request or email/pass parameters '''
    if email == "" and req is not None:
      json_data = api.get_json(req)
      email = json_data['email']
      password = json_data['password']

    user = Users.get(email.lower())
    if isinstance(user, Exception):
      return api.error(user)
    elif password == decrypt(user.key):
      console.log(f"User {user.uuid} logged in")
      return api.data({'uuid': user.uuid, 'email': user.email, 'session': user.session})

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
