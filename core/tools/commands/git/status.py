# Overlord library
from web.settings import CLIENT_DATA
from core.library import console


def app() -> str:
  """
  Check the git status of the main app repository
  """
  print()
  return console.input("git status")


def clients(client) -> str:
  """
  Check the git status of the main app repository
  """
  print()
  if client == 'all':
    for _client in CLIENT_DATA:
      console.out(_client, "green")
      console.input("git status", cwd=CLIENT_DATA[_client]['src'])
  elif client in CLIENT_DATA:
    console.input("git status", cwd=CLIENT_DATA[client]['src'])
  else:
    console.out(f"[ERROR] No client found matching input `{client}`", colour="red")
