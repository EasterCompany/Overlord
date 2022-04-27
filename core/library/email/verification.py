# Overlord library
from core.library import email
# Overlord web
from web.settings import SECRET_DATA


def send(target, key, domain):
    """
    Sends a user verification email to the target

    :param target str: target email address for verification
    :param key str: target user verification key
    :param domain str:
    """
    with open(__file__.replace('verification.py', 'templates/verification.html'), "r") as template:
        # Generate context
        url = "http://localhost:8000" if domain.startswith('localhost:') else "https://" + domain

        # Render template context
        context = template.read().\
            replace('<url/>', url).\
            replace('<target/>', target).\
            replace('<key/>', key).\
            replace('<domain/>', domain).\
            replace('<from/>', SECRET_DATA['EMAIL_USER'])

        # Send email
        return email.send(
            Target=target,
            Subject=f"[{domain}] User Email Verification",
            Body=context
        )
