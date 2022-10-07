from core.library import uuid


def check_uuid_exists(model, uuid):
    """
    Checks weather a uuid already exists

    :param uuid str: uuid to check if already exists
    :return bool: true or false statement which is true when it does already exist
    """
    return model.objects.filter(uuid=uuid).count() > 0


def generate_new_uuid(model):
    """
    Generates a new uuid, checks that it doesn't already exist (retries with another generation if it does)
    and returns a `unique` string representing a uuid for a new entry if it doesn't already exist.

    :return str: universal unique identification string containing 36 characters (32 hex digits + 4 dashes)
    """
    new_uuid = uuid()
    while check_uuid_exists(model, new_uuid):
        new_uuid = uuid()
    return new_uuid
