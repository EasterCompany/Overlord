# Overlord library
from web.settings import CLIENT_DATA, BASE_DIR
from core.library import console


def app() -> str:
  """
  Check the git status of the main app repository
  """
  print()
  return console.input("git status", cwd=BASE_DIR, show_output=True)


def clients(client) -> str:
  """
  Check the git status of the main app repository
  """
  print()
  if client == 'all':
    for _client in CLIENT_DATA:
      console.out(_client, "green")
      console.input("git status", cwd=CLIENT_DATA[_client]['src'], show_output=True)
  elif client in CLIENT_DATA:
    console.input("git status", cwd=CLIENT_DATA[client]['src'], show_output=True)
  else:
    console.out(f"[ERROR] No client found matching input `{client}`", colour="red")
