# Overlord library
from core.library import api
# Overlord api
from api.user import session
from api.models import UserDetails, UserAuth


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


def create_new_user_data(email, key, permissions):
    # Email Exists
    if UserAuth.objects.filter(email=email).count() > 0:
        return api.std(message="Email already exists", status=api.BAD)
    # Create User
    UserAuth.objects.create(
        email=email,
        key=key,
        permissions=int(permissions),
        session=session.generate()
    )
    return api.std(message="Success!", status=api.OK)
