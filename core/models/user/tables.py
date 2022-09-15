# Standard library
from uuid import uuid1
# Django library
from django.db import models
# Overlord library
from core.library import time

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
        default=uuid1,
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

    [first_names] any string provided by the user
        +   optional field
    [middles_names] any string provided by the user
        +   optional field
    [last_name] any string provided by the user
        +   optional field
    [display_image] a string containing a url to an image file
        +   optional field
    [display_name] how this user is known to other users
        +   optional field which defaults to the users email address
    [date_of_birth] day of birth
        +   required field provided by the user on registration
    [date_joined] day of account creation
        +   required field which defaults to the current date
    """
    first_name = models.TextField(default="")
    middle_names = models.TextField(default="")
    last_name = models.TextField(default="")

    display_image = models.TextField(default="")
    display_name = models.TextField(null=True, blank=True, default="")

    date_of_birth = models.DateField(null=False, blank=False)
    date_joined = models.DateField(null=False, blank=False, default=time.get_datetime_str)


class UserAuth(UserModel):
    """
    Contains information to login and maintain a session with the session;
    A new user session is generated upon each login or registration request.

    [email]
        +   unique email address provided by the user
    [key]
        +   an encrypted password provided by the user
    [session_token] 128 character randomly generated string
        +   used by the user to begin a `new session` on the same device
        +   *NEVER CHANGES*
    [refresh_token] 32 character randomly generated string
        +   used by the user to make requests during a session
        +   *RANDOMLY GENERATED UPON EVERY NEW SESSION*
    [last_activity]
        +   datetime string as such `YEAR-MONTH-DAY HOUR:MINUTE:SECOND.MILLISECOND`
        +   *UPDATED EVERY TIME A REQUEST IS MADE*
    [user_device_id]
        +   the id of the device the user has registered with this session
        +   the device id of a session must be provided in the initial
            request with the session token and cannot change
        +   *NEVER CHANGES*
    [panels] e-panels which this user can view
        +   required field which defaults to an empty string
    """
    email = models.TextField(null=False, blank=False, unique=True)
    sms = models.TextField(unique=True, null=True, blank=True)
    key = models.TextField(null=False, blank=False)

    authenticated_email = models.BooleanField(default=False)
    authenticated_sms = models.BooleanField(default=False)

    permissions = models.IntegerField(null=True, blank=True)
    session = models.TextField(null=False, blank=False, unique=True)
    last_activity = models.DateTimeField(null=False, blank=False, default=time.get_datetime_str)
    active = models.BooleanField(null=False, blank=False, default=False)

    panels = models.TextField(null=False, blank=False, default="")
