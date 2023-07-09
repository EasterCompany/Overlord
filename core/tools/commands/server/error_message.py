from core.library import console
from web.settings import SECRET_DATA


def error_message():
  if len(SECRET_DATA['SERVER_URL']) >= 3:
    return console.out('''
  `SERVER` tools requires the `SERVER_URL` field in your
  `.config/secret.json` file to contain the domain name
  of the server you want to interact with.

  ie; www.example.com

  Do not include the protocol (http / https) in the string.''', 'yellow')

  return console.out('''
  `SERVER:` commands require a valid command following them.

  server:<command> -<argument>

  Using this command allows you to execute Overlord CLI commands
  on the server remotely.''', 'yellow')
