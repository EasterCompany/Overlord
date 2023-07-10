from core.library import console
from web.settings import SECRET_DATA


def error_message() -> str:
  if len(SECRET_DATA['SERVER_URL']) >= 3:
    return console.out('''
  `SERVER` tool requires the `SERVER_URL` field in your
  `.config/secret.json` file to contain the domain name
  of the server you want to interact with.

  ie; www.example.com

  Do not include the protocol (http / https) in the string.''', 'yellow')

  return console.out('''
  `server` command requires a valid command following it.

  server:<command> -<argument>

  Using this command allows you to execute Overlord CLI commands
  on the server remotely.''', 'yellow')


def no_server_cmd_error_message() -> str:
  return console.out('''
  `server` command cannot use the `server` command on the
  remote server.''', 'yellow'
  )
