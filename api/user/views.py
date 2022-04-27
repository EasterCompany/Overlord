# Standard library
from urllib import parse
# Overlord library
from core.library import api
# Overlord tools
from tools.assets.settings import ADMIN_EMAIL, SECRET_KEY
# Overlord api
from api.user import session, controls
from api.models import UserAuth, UserDetails


def delete(req, uuid, *args, **kwargs):
    """
    Purges all user data related to a uuid - the User model is a source of truth for weather a user exists
    and there for must always be the last table to be purged of user data & the first to be appended with data

    :param uuid str: unique identifier for user
    :return bool: true if user data was successfully purged
    """
    if UserAuth.objects.filter(uuid=uuid).count() > 0:
        try: UserAuth.objects.filter(uuid=uuid).delete()
        except Exception as exception: return api.std(message=str(exception), status=api.BAD)
        try: UserDetails.objects.filter(uuid=uuid).delete()
        except Exception as exception: return api.std(message=str(exception), status=api.BAD)
        return api.std(message="success", status=api.OK)
    return api.std(message="failed", status=api.BAD)


def list_all(req, *args, **kwargs):
    """
    Returns a list of all UUID and Email combinations within the database

    [   ["UUID", "Email" ... ] <-- Table Headers
        [[], [],  [], [] ... ] <-- Table Row & Data ]

    formated for use with a table

    H1          H2          H3
    -------     -------     -------
    ..          ..          ..
    ..          ..          ..
    """

    def __body__(body_query):
        body_row_data = []

        for user in body_query:
            body_row_data.append([
                str(user),
                user.email,
                user.last_activity,
                "✔️" if user.active else "❌"
            ])

        return body_row_data

    return api.table(
        Table=UserAuth,
        Headers=['UUID', 'Email', 'Last Active', 'Authenticated'],
        Body=__body__,
        filter={ "order_by": "-last_activity" }
    )


def view(req, uuid, *args, **kwargs):
    """
    Returns a dictionary (key: header for section, value: [field, field_value])

    {
        Details: ['name', name], ['age', age] ...
        ...
    }

    formatted for output on a text form

    :param uuid str: unique identifier
    :return: api.std
    """
    try:
        user = UserAuth.objects.filter(uuid=uuid).only()
        user = {'Email': user.email}
    except Exception as exception:
        return api.std(
            status=api.BAD,
            message={'error': str(exception)}
        )

    try:
        details = UserDetails.objects.filter(uuid=uuid).only()
    except Exception as exception:
        return api.std(
            status=api.BAD,
            message={'error': str(exception)}
        )

    return api.std(
        status=api.OK,
        message=[ user, details ]
    )


def create(req, email="", key="", permissions=0, *args, **kwargs):
    """
    Create a new user using a unique email address

    :param email str: unique user email input
    :param key str: pre-hashed user password key
    :return: api.std
    """
    # Consume Input
    email = parse.unquote(email)
    key = req.body.decode('utf-8')
    permissions = parse.unquote(permissions)
    # Create User
    controls.create_new_user_data(email, key, permissions)
    # Standard Response
    return api.std(message="Success!", status=api.OK)


def verify(req, target, key, *args, **kwargs):
    """
    Complete user registration and verify email

    :param target str: unique user email address
    :param key str: unique user verification key
    :return: api.std
    """
    try:
        user = UserAuth.objects.get(email=target, key=key, active=False)
    except Exception as exception:
        return api.std(message=str(exception), status=api.BAD)

    user.active = True
    user.authenticated_email = True
    session.new(user)

    return api.std(message="Successfully verified user email address!", status=api.OK)


def login(req, emailURI, *args, **kwargs):
    """
    Generate a new Refresh & Session Token for the user identified by the uuid parameter

    :param uuid str: unique identifier for user
    :param key str: encrypted login secret key
    :return: api.std
    """
    # Admin User Login
    try:
        email = parse.unquote(emailURI)
        key = req.body.decode('utf-8')

        if email == ADMIN_EMAIL:
            admin_query = UserAuth.objects.filter(email=email, key=key)

            if UserAuth.objects.filter(email=email).count() == 0 and key == SECRET_KEY:
                print("""\n     [CREATING.. E-PANEL ADMIN]     \n""")
                controls.create_new_user_data(email, key, "99")
                admin_query = UserAuth.objects.filter(email=email, key=key)

            if admin_query.count() == 1:
                print("""\n     [LOGGING... E-PANEL ADMIN]     \n""")
                new_sesh = session.generate()
                admin = admin_query.first()
                admin.session = new_sesh
                admin.save()
                session_json = {
                    "uuid": admin.uuid, "email": admin.email, "sms": admin.sms, "key": admin.key,
                    "auth_email": admin.authenticated_email, "auth_sms": admin.authenticated_sms,
                    "session": admin.session, "last_activity": admin.last_activity,
                    "active": admin.active, "permissions": admin.permissions
                }
                return api.std(api.OK, session_json)

            else:
                return api.error()

    except Exception as exception:
        return api.error(exception)

    # Regular User Login
    try:
        user = UserAuth.objects.filter(email=email, key=key).first()
        sesh = session.generate()
        user.session = sesh
        user.save()
        return api.std(api.OK, sesh)

    except Exception as exception:
        return api.error(exception)


def edit(req, *args, **kwargs):
    """
    Edit a user based on the given email address

    :param email str: unique user email address
    :return: edit & save user database object
    """
    try:
        user = UserAuth.objects.filter(session=req.headers.get('Authorization')).only()
        user.email = req.post.get('email')
        details = UserDetails.objects.filter(uuid=user.uuid).only()
        details.first_name = req.post.get('first_name')
        details.last_name = req.post.get('last_name')
        details.display_name = req.post.get('display_name')
        return api.std(message="User database records successfully modified", status=api.OK)
    except Exception as exception:
        return api.std(api.BAD, exception)
