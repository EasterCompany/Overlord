# Std library
import os
from datetime import date
# Overlord library
from core.library import console
from web.settings import BASE_DIR, CLIENT_DATA

COMMIT_DATE = date.today().strftime("%d/%b/%y")
AUTO_COMMIT_MESSAGE=f"🤖 [AUTO] {COMMIT_DATE}".upper()


def all():
  """
  Pushes the latest changes to & from every repository found within this projects scope
  """
  os.chdir(BASE_DIR)

  console.out("\nOverlord", "yellow")
  print("-------------------------\n")
  os.system(f'''git add . && git commit -m "{AUTO_COMMIT_MESSAGE}" && git push''')
  print("\n")

  for client in CLIENT_DATA:
    source_dir = CLIENT_DATA[client]["src"]
    source_api = BASE_DIR + f'/api/{client}'

    if os.path.exists(f"{source_dir}/.git"):
      console.out(f"\n{client.title()}", "yellow")
      print("-------------------------\n")
      os.chdir(source_dir)
      os.system(f'''git add . && git commit -m "{AUTO_COMMIT_MESSAGE}" && git push''')
      os.chdir(BASE_DIR)
      print("\n")

    if os.path.exists(f"{source_api}/.git"):
      console.out(f"\n{client.title()} (API)", "yellow")
      print("-------------------------\n")
      os.chdir(source_api)
      os.system(f'''git add . && git commit -m "{AUTO_COMMIT_MESSAGE}" && git push''')
      os.chdir(BASE_DIR)
      print("\n")
