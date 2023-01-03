# Std library
import os
from datetime import date
# Overlord library
from core.library import console, time, version
from web.settings import BASE_DIR, CLIENT_DATA

current_version = version.Version()
COMMIT_DATE = date.today().strftime("%d/%b/%y")
AUTO_COMMIT_MESSAGE=f'🤖 [AUTO] {current_version} {time.timestamp()}'


def all():
  """
  Pushes the latest changes to & from every repository found within this projects scope
  """
  os.chdir(BASE_DIR)

  console.out("\nOVERLORD", "yellow")
  print("-------------------------")
  os.system(f'''git add . && git commit -m "{AUTO_COMMIT_MESSAGE}" && git push''')

  for client in CLIENT_DATA:
    print("\n")
    source_dir = CLIENT_DATA[client]["src"]
    source_api = BASE_DIR + f'/api/{client}'

    if os.path.exists(f"{source_dir}/.git"):
      console.out(f"{client.upper()} (CLIENT)", "yellow")
      print("-------------------------")
      os.chdir(source_dir)
      os.system(f'''git add . && git commit -m "{AUTO_COMMIT_MESSAGE}" && git push''')
      os.chdir(BASE_DIR)
      print("\n")

    if os.path.exists(f"{source_api}/.git"):
      console.out(f"{client.upper()} (API)", "yellow")
      print("-------------------------")
      os.chdir(source_api)
      os.system(f'''git add . && git commit -m "{AUTO_COMMIT_MESSAGE}" && git push''')
      os.chdir(BASE_DIR)
