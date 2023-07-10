# Standard library
import requests
# Overlord library
from core.library import console
from web.settings import SECRET_DATA


def post_command(command:str, arguments:list|None = None) -> None:
  ''' Posts a command request to a remote servers external command endpoint '''
  console.out("\n> Server Command")
  console.out(f"  {console.wait} executing...", end="\r")

  if arguments is None:
    arguments = []
  for index, arg in enumerate(arguments):
    if not arg.startswith('-'):
      arguments[index] = f'-{arg}'
  command_line = [ command, ] + arguments

  try:
    response = requests.post(
      f"https://{SECRET_DATA['SERVER_URL']}/api/o-core/external-command",
      headers={
        "Content-Type": "application/json; charset=utf-8"
      },
      json={
        "pub_key": SECRET_DATA['SERVER_KEY'],
        "cmd_line": command_line
      },
      timeout=600
    )
  except requests.exceptions.Timeout:
    console.out(f"  {console.failure} Connection to server timed out.")
    return

  status = response.status_code
  data = 500
  output = None

  if response.headers['Content-Type'] == 'application/json':
    data = response.json()
    if 'status' in data:
      status = data['status']
    if 'data' in data:
      data = data['data']
      if 'message' in data and 'output' in data:
        data = data['message']
        output = data['output']
  else:
    data = str(response.content, 'utf-8')

  console.out(f"                             ", end="\r")
  console.out(
    f"  STATUS: {console.status(status)}\n"
    f"  DATA: {console.status(status, data)}"
  )

  if output is not None:
    for line in output:
      print(line[0], end=line[1])
