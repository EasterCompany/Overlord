# Standard library
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Overlord library
from core.library.email import (
    verification,
)

# Overlord web
from web.settings import SECRET_DATA


def send(Target='', Subject='', Body=''):
    email = SECRET_DATA["EMAIL_USER"] or None
    epass = SECRET_DATA["EMAIL_PASS"] or None

    mail_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    mail_ssl.ehlo()
    mail_ssl.login(email, epass)

    heading = MIMEText(
        f'From: No Reply <{email}>\nTo: <{Target}>\nSubject:{Subject}\n\n',
        'plain'
    )
    content = MIMEText(
        Body,
        "html"
    )

    message = MIMEMultipart("alternative")
    message["Subject"] = Subject
    message["From"] = email
    message["To"] = [ Target, ]

    message.attach(heading)
    message.attach(content)

    mail_ssl.sendmail(email, Target, content.as_string())
    mail_ssl.close()
