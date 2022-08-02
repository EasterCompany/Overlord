# Standard library
from cryptography.fernet import Fernet
from rsa import decrypt, encrypt
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


def create_new_user_data(email, password, permissions):
    # Check if email already exists
    if UserAuth.objects.filter(email=email).count() > 0:
        return api.std(message="Email already exists", status=api.BAD)
    # Encrypt password
    encrypted_password = Fernet.encrypt(password)
    print(encrypted_password)
    decrypted_password = Fernet.decrypt(encrypted_password)
    print(decrypted_password)
    # Create new user
    UserAuth.objects.create(
        email=email,
        key=password,
        permissions=int(permissions),
        session=session.generate()
    )
    return api.std(message="Success!", status=api.OK)
