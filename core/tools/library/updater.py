# Standard library
import time
import atexit
import random
import shutil
import requests
import logging
from hashlib import md5
# Overlord library
from web.settings import BASE_DIR
from core.library.version import Version
from core.library import exists, mkdir, json, console
version = Version()
update_logger = None
update_logger_dir = f'{BASE_DIR}/.logs'
update_logger_path = f'{BASE_DIR}/.logs/update_logger'
random_file_name = f"{random.randint(1000, 9999)}".encode()
random_file_hash = md5(random_file_name).hexdigest()
temp_directory = f"{BASE_DIR}/.temp-overlord-update"
temp_update_path = f"{temp_directory}/{random_file_hash}"

# Create the logs directory if it doesn't exist
if not exists(update_logger_dir):
  mkdir(update_logger_dir)

# Create the log file if it doesn't exist
if not exists(update_logger_path):
  with open(update_logger_path, 'w') as update_logger_file:
    default_log = {
      'last_check': [0, version.major, version.minor, version.patch]
    }
    update_logger_file.write(json.dumps(default_log, indent=2))


def read_update_logger() -> dict:
  """
  Read the update logger file and import it's contents into memory

  :return dict:
  """
  global update_logger
  with open(update_logger_path, 'r') as update_logger_file:
    update_logger = json.loads(update_logger_file.read())


# Read the log file is it hasn't already been read
if update_logger is None:
  read_update_logger()


def save_update_logger() -> None:
  """
  Save the update logger to the file so it's contents can be saved

  :return None:
  """
  global update_logger
  update_logger['last_check'][0] = time.time()
  with open(update_logger_path, 'w') as update_logger_file:
    update_logger_file.write(json.dumps(update_logger, indent=2))


def get_latest_version_label(force:bool = False) -> list:
  """
  Check the web for the latest version of Overlord which is available

  :return list:
  """
  global update_logger
  last_major = update_logger['last_check'][1]
  last_minor = update_logger['last_check'][2]
  last_patch = update_logger['last_check'][3]
  last_version = [last_major, last_minor, last_patch]

  if update_logger['last_check'][0] + 10800 > time.time() and not force:
    return last_version

  response = requests.get("https://raw.githubusercontent.com/EasterCompany/RDFS/Prd/Overlord/latest_ver")

  if not response.status_code == 200:
    return last_version

  try:
    ver_list = response.content.decode('utf-8').split('.')
    update_logger['last_check'][1], update_logger['last_check'][2], update_logger['last_check'][3] = \
      int(ver_list[0]), int(ver_list[1]), int(ver_list[2])
    save_update_logger()
    return int(ver_list[0]), int(ver_list[1]), int(ver_list[2])
  except:
    return last_version


def check_status(force:bool = False) -> list:
  """
  Checks the latest version and return an update availability status which can be
  displayed inside the CLI.

  :return list: [ status : boolean, status : string ]
  """
  latest_version = get_latest_version_label(force=force)
  new_major = version.major < int(latest_version[0])
  new_minor = new_major == False and version.minor < int(latest_version[1])
  new_patch = new_minor == False and version.patch < int(latest_version[2])
  update_available = new_major or new_minor or new_patch

  if not update_available:
    return False, console.out("This instance is currently up-to-date.", "green", False)

  new_version = console.out(f"v{latest_version[0]}.{latest_version[1]}.{latest_version[2]}", "green", False)
  if new_minor or new_major:
    cur_version = console.out(f"v{version.major}.{version.minor}.{version.patch}", "red", False)
  else:
    cur_version = console.out(f"v{version.major}.{version.minor}.{version.patch}", "yellow", False)

  return True, f"`{cur_version}` -> `{new_version}`"


def purge_temp_directory() -> None:
  """
  If the temporary directory exists then it is deleted

  :return None:
  """
  if exists(temp_update_path):
    shutil.rmtree(temp_update_path)
  if exists(temp_directory):
    shutil.rmtree(temp_directory)


def _log_path(path, names):
  logging.info(f'Installing {path} ...')
  return []


def clone_latest_version() -> None:
  """
  Clones the latest version from the production branch of the Overlord repository to
  a temporary directory

  :return None:
  """
  atexit.register(purge_temp_directory)
  purge_temp_directory()

  try:
    console.out("  Downloading Update ... ", end="\r")
    mkdir(temp_directory)
    console.input(
      f"cd {temp_directory} && "
      f"git clone --quiet --single-branch --branch Prd --depth=1 git@github.com:EasterCompany/Overlord.git "
      f"{random_file_hash}"
    )
    console.out("  ✅ Downloaded Update   ", "success")
    console.out("  Installing Update ...  ")
    shutil.copytree(temp_update_path, BASE_DIR, ignore=_log_path)
    shutil.move(temp_update_path, BASE_DIR)
    console.out("  ✅ Installed Update Successfully!", "success")
  except Exception as update_error:
    purge_temp_directory()
    console.out(f"\n  Failed to update due an unexpected error\n  {update_error}")
    return False

  purge_temp_directory()
  atexit.unregister(purge_temp_directory)
  return True
