# Standard library
from cryptography.fernet import Fernet
# Overlord library
from web.settings import SECRET_DATA

ENGINE = Fernet(bytes(SECRET_DATA['SERVER_KEY'], 'utf-8'))


def encrypt(data):
  if not isinstance(data, bytes):
    data = bytes(str(data), 'utf-8')
  return ENGINE.encrypt(data)


def decrypt(data):
  return ENGINE.decrypt(data).decode('utf-8')
