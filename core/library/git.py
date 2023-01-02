# Overlord library
from web.settings import PRODUCTION_BRANCH
from core.library import console, time, version
current_version = version.Version()


def branch(repo_path:str) -> str:
  """
  Detect which branch you are currently on in a Git repository

  :return str: name of current branch
  """
  branch_name = console.input('git rev-parse --abbrev-ref HEAD', cwd=repo_path, show_output=False).stdout
  branch_name = branch_name.strip()
  return branch_name


def sync(repo_path:str) -> None:
  """
  This function uses the console.input method to run pull and push commands on the repository located at repo_path.
  The output of the commands is printed to the console.

  You can call this function like this: git_pull_push('/path/to/repo')
  Make sure that the repository is properly set up and that you have access to it before running this function.

  :param repo_path str: path to the target repository
  :return None:
  """
  console.input('git pull -f', cwd=repo_path, show_output=True)
  console.input('git add .', cwd=repo_path, show_output=True)
  console.input(f'git commit -m "🤖 [AUTO] {current_version} {time.timestamp()}"', cwd=repo_path, show_output=True)
  console.input('git push -f', cwd=repo_path, show_output=True)


def checkout(repo_path:str, target:str = PRODUCTION_BRANCH) -> None:
  """
  Sync the current branch and then switch branch from the repo_path onto the target branch

  :param repo_path str: path to the target repository
  :param target str: name of the target branch
  :return None:
  """
  console.input(f'git checkout {target}', cwd=repo_path, show_output=True)


def merge(repo_path:str, target:str = PRODUCTION_BRANCH) -> None:
  """
  Sync the current branch, checkout target branch and then pull from the branch you were previously on.
  The out of the commands is printed to the console.

  :param repo_path str: path to the repo you wish to merge
  :param target str: name of the target branch
  :return None:
  """
  branch_name = branch(repo_path)
  sync(repo_path)
  checkout(repo_path, target)
  sync(repo_path)
  console.input(f'git pull origin {branch_name}', cwd=repo_path, show_output=True)
  sync(repo_path)
