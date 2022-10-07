# Standard library
from urllib import parse
# Overlord library
from core.library import api
from core.library.cryptography import decrypt
from core.model.user import session, controls
from core.model.user.tables import UserAuth, UserDetails



def list_all(req, *args, **kwargs):
    """
    Returns a list of all UUID and Email combinations within the database

    [   ["UUID", "Email" ... ] <-- Table Headers
        [[], [],  [], [] ... ] <-- Table Row & Data ]

    formatted for use with a table

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
        return api.error(exception)

    user.active = True
    user.authenticated_email = True
    session.new(user)

    return api.std(message="Successfully verified user email address!", status=api.OK)


def login(req, emailURI, *args, **kwargs):
    """
    Generate a new session token and return it if the email and password combination
    match and existing user record.

    :param uuid str: unique identifier for user
    :param key str: encrypted login secret key
    :return: api.std
    """
    email = parse.unquote(emailURI).strip()
    password = req.body.decode('utf-8')
    user = UserAuth.objects.filter(email=email).first()
    user.session = session.generate()
    user.save()

    if user and password == decrypt(user.key):
        return api.data({
            'uuid': user.uuid, 'email': user.email, 'session': user.session
        })

    return api.error()


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
        return api.error(exception)
