# Django library
from django.utils.crypto import get_random_string
# Overlord library
from core.library import api, time
# Overlord api
from api.models import UserAuth


def authenticate(req, permission='', *args, **kwargs):
    """
    return boolean indicating the given token authentication status

    :param token str:
    :return boolean:
    """
    print(req.META['HTTP_AUTHORIZATION'])
    try:
        user = UserAuth.objects.get(session=req.META['HTTP_AUTHORIZATION'])
        if user.active and permission == '':
            return True
        return user.active and (permission in user.permissions or 'admin+' in user.permissions)
    except:
        pass
    return False


def generate():
    """
    Generate a session token

    :param uuid str: identifier
    :param authenticated bool: weather user is authenticated
    :param active bool: weather this user is active or disabled
    """
    return f"{get_random_string(128)} ~/~ {time.get_datetime_str()} ~/~ 0"


def _is_authenticated(user):
    """
    :param user model: user object for checking
    :return boolean: user authenticated via email or sms
    """
    if user.authenticated_email or user.authenticated_sms:
        return True
    return False


def refresh(token):
    # Select User
    user = UserAuth.objects.get(session=token)

    if user.active:
        # Generate New Token
        session = generate(user.email, _is_authenticated(user), user.active)

        # Save New Token
        user.last_activity = time.get_datetime_str()
        user.session = session
        user.save()

        # Standard Response
        return api.std(
            status=api.OK,
            message=session
        )

    # Standard Response
    return api.std(
        status=api.BAD,
        message="user disabled"
    )
