# Std library
import os
from datetime import date
# Overlord library
from core.library import console, time, version, listdir, isdir
from web.settings import BASE_DIR, CLIENT_DATA, PROJECT_NAME

current_version = version.Version()
COMMIT_DATE = date.today().strftime("%d/%b/%y")
AUTO_COMMIT_MESSAGE=f'🤖 [AUTO] {current_version} {time.timestamp()}'


def all():
  ''' Pushes the latest changes to & from every repository found within this projects scope '''
  os.chdir(BASE_DIR)

  console.out(f"\n{PROJECT_NAME.upper()}\n-------------------------", "yellow")
  os.system(f'''git add . && git commit -m "{AUTO_COMMIT_MESSAGE}" && git push''')

  pushed_apis = []
  api_dir = f"{BASE_DIR}/api"

  for client in CLIENT_DATA:
    source_dir = CLIENT_DATA[client]["src"]
    source_api = BASE_DIR + f'/api/{client}'

    if os.path.exists(f"{source_dir}/.git"):
      console.out(f"{client.upper()} (CLIENT)\n-------------------------", "yellow")
      os.chdir(source_dir)
      os.system(f'''git add . && git commit -m "{AUTO_COMMIT_MESSAGE}" && git push''')
      os.chdir(BASE_DIR)
      print("\n")

    if os.path.exists(f"{source_api}/.git"):
      console.out(f"{client.upper()} (API)\n-------------------------", "yellow")
      os.chdir(source_api)
      os.system(f'''git add . && git commit -m "{AUTO_COMMIT_MESSAGE}" && git push''')
      os.chdir(BASE_DIR)
      pushed_apis.append(client)

  potential_apis = listdir(api_dir)
  for dir in potential_apis:
    if (dir_path := f"{BASE_DIR}/api/{dir}") and isdir(dir_path) and (contents := listdir(dir_path)):
      if '.git' in contents and dir not in pushed_apis:
        console.out(f"{dir.upper()} (API)\n-------------------------", "yellow")
        os.chdir(dir_path)
        os.system(f'''git add . && git commit -m "{AUTO_COMMIT_MESSAGE}" && git push''')
        os.chdir(BASE_DIR)
