# Standard library
from cryptography.fernet import Fernet
# Overlord library
from web.settings import SECRET_DATA
from core.library import console

# Generates a fernet instance using the server key
try:
  ENGINE = Fernet(bytes(SECRET_DATA['SECRET_KEY'], 'utf-8'))
except:
  console.out(
    "\n  [ERROR] Server Key is not a 32 character url-safe string\n",
    "red"
  )
  exit()


def encrypt(data) -> str:
  """
  Encrypt almost any datatype and return it as a string

  :param data str|bytes|int|float: raw data
  :return str: encrypted string
  """
  if not isinstance(data, bytes):
    data = bytes(str(data), 'utf-8')
  return ENGINE.encrypt(data).decode('utf-8')


def decrypt(data) -> str:
  """
  Decrypt almost any datatype and return it as a string

  :param data str|bytes|int|float: encrypted data
  :return str: raw data
  """
  if not isinstance(data, bytes):
    data = bytes(str(data), 'utf-8')
  return ENGINE.decrypt(data).decode('utf-8')
