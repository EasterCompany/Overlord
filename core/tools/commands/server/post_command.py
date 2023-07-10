# Standard library
import requests
# Overlord library
from core.library import console
from web.settings import SECRET_DATA


def post_command(command, arguments) -> None:
  console.out("\n> Execute Server Command")
  console.out(f"  {console.wait} waiting...", end="\r")

  response = requests.post(
    f"https://{SECRET_DATA['SERVER_URL']}/api/o-core/external-command",
    headers={
      "Content-Type": "application/json; charset=utf-8"
    },
    json={
      "pub_key": SECRET_DATA['SERVER_KEY'],
      "cmd_line": [ command, ] + arguments
    }
  )

  status = response.status_code #if 'status' not in response.json else response.json['status']
  if response.headers['Content-Type'] == 'application/json':
    data = response.json()
    if 'status' in data:
      status = data['status']
    if 'data' in data:
      data = data['data']
  else:
    data = response.content

  console.out(f"                           ", end="\r")
  console.out(
    f"  STATUS: {console.status(status)}\n"
    f"  DATA: {console.status(status, data)}"
  )
