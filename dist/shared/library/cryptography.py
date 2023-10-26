from shared.library import Fernet, settings, console

try:
  ENGINE = Fernet(bytes(settings.SECRET_KEY, 'utf-8'))
except:
  console.out(
    "\n  [ERROR] Server Key is not a 32 character url-safe string\n",
    "red"
  )
  exit()


def encrypt(data) -> str:
  if not isinstance(data, bytes):
    data = bytes(str(data), 'utf-8')
  return ENGINE.encrypt(data).decode('utf-8')


def decrypt(data) -> str:
  if not isinstance(data, bytes):
    data = bytes(str(data), 'utf-8')
  return ENGINE.decrypt(data).decode('utf-8')
