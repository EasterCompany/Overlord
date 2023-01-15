# Overlord library
from web.settings import BASE_DIR
from core.library import console, exists, is_alphanumeric, to_alphanumeric


def download_repo(repo_link, name):
  """
  Downloads a git repository with a given name
  """
  console.out(f"  {console.wait} Downloading ... ", end="\r")
  console.input(f"git clone {repo_link} {name}", cwd=BASE_DIR+'/clients')
  console.out(f"  ✅ Downloaded                  ", "success")


def create(name:str, git_repo:str = None, standalone:bool = False) -> None:
  """
  Creates a Universal API from either a basic template if the the given name
  is an existing client without an associated API, git repository if the given
  name is a git HTML/SSH link or a basic template if the given name is unique
  and the user is trying to create a standalone API

  :param name str: keyword is either an associated client or standalone name
  :return None:
  """
  if not is_alphanumeric(name):
    console.out(
      "\n[WARNING] Client names may only contain alphanumeric characters\n"
      "          including underscores and must be URL safe.\n\n"
      "          Any non-alphanumeric or underscore characters will be\n"
      "          purged from the name.",
      "yellow"
    )
    name = to_alphanumeric(name)

  # Existing Client Match / Standalone API
  if not exists(f'clients/{name}'):
    console.out(
      f"\n[WARNING] Client with name `{name}` does not exist.\n"
       "          This will create a standalone universal API\n"
       "          enter 'Y' to continue or 'N' to cancel."
    )
    standalone = input("\nMake Standalone API & Continue (Y/N):").lower() == 'y'
    if not standalone: return None

  #
