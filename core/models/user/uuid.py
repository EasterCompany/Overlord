# Standard library
from uuid import uuid1


def check_uuid_exists(uuid_string):
    """
    Checks weather a uuid already exists

    :param uuid str: uuid to check if already exists
    :return bool: true or false statement which is true when it does already exist
    """
    from api.models import UserAuth
    return UserAuth.objects.filter(uuid=uuid_string).count() > 0


def generate_new_uuid():
    """
    Generates a new uuid, checks that it doesn't already exist (retries with another generation if it does)
    and returns a `unique` string representing a uuid for a new user if it doesn't already exist.

    :return str: unique user identification string containing 36 characters (32 hex digits + 4 dashes)
    """
    new_uuid = uuid1()

    while check_uuid_exists(new_uuid):
        new_uuid = uuid1()

    return new_uuid
