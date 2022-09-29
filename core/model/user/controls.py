# Overlord library
from core.library import api
from core.library.cryptography import encrypt
from core.model.user import session
from core.model.user.tables import UserDetails, UserAuth


def purge_all_user_data(uuid):
    """
    Purges all user data related to a uuid

    :param uuid str: unique identifier for user
    :return bool: true if user data successfully purged
    """
    if UserAuth.objects.filter(uuid=uuid).count > 0:
        try:
            UserDetails.objects.filter(uuid=uuid).delete()
            UserAuth.objects.filter(uuid=uuid).delete()
            print(f"[USER] Successfully purged user data for <user: {uuid}>")
            return True
        except Exception as exception:
            print(f"[USER] Failed to purge data for <user: {uuid}>\n{exception}\n\n")
    return False


def create_new_user_data(email, password, permissions):
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


def verify_identity(email, session):
    if UserAuth.objects.filter(email=email, session=session).count() == 0:
        return api.error("User with that session does not exist.")
    return api.success()


def authorized(uuid, sesh):
    return UserAuth.objects.filter(uuid=uuid).only()[0].session.split("[:~OLT~:]")[1] == sesh


def if_authorized(req, do_function):
  try:
    auth_uuid, auth_sesh = api.get_user(req)
    if authorized(auth_uuid, auth_sesh):
        r = do_function()
        if isinstance(r, bool):
            return api.success() if r is True else api.error()
        elif isinstance(r, dict) or isinstance(r, list) or \
            isinstance(r, int) or isinstance(r, float) or \
            isinstance(r, str):
            return api.data(r)
        return api.success()
    return api.error("Unauthorized access.")
  except Exception as exception:
    return api.error(exception)
