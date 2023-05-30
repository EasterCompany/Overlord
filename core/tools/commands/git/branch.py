import os
from web.settings import BASE_DIR, PROJECT_NAME, CLIENT_DATA
from core.library import console, listdir, isdir


def switch_all(target:str) -> None:
  ''' Recursively switches all repositories within the project to a specific branch '''
  os.chdir(BASE_DIR)

  console.out(f"\n{PROJECT_NAME.upper()}\n-------------------------", "yellow")
  os.system(f"git checkout {target}")

  pulled_apis = []
  api_dir = f"{BASE_DIR}/api"

  for client in CLIENT_DATA:
    print("\n")
    source_dir = CLIENT_DATA[client]["src"]
    source_api = BASE_DIR + f'/api/{client}'

    if os.path.exists(f"{source_dir}/.git"):
      console.out(f"{client.upper()} (CLIENT)\n-------------------------", "yellow")
      os.system(f"cd {source_dir} && git pull --recurse-submodules && cd {BASE_DIR}")
      print("\n")

    if os.path.exists(f"{source_api}/.git"):
      pulled_apis.append(client)
      console.out(f"{client.upper()} (API)\n-------------------------", "yellow")
      os.system(f"cd {source_api} && git pull --recurse-submodules && cd {BASE_DIR}")

  potential_apis = listdir(api_dir)
  for dir in potential_apis:
    if (dir_path := f"{BASE_DIR}/api/{dir}") and isdir(dir_path) and (contents := listdir(dir_path)):
      if '.git' in contents and dir not in pulled_apis:
        console.out(f"{dir.upper()} (API)\n-------------------------", "yellow")
        os.system(f"cd {dir_path} && git pull --recurse-submodules && cd {BASE_DIR}")
