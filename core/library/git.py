# Overlord library
from web.settings import PRODUCTION_BRANCH
from core.library import console, time, version
current_version = version.Version()


def branch(repo_path:str) -> str:
  """
  Detect which branch you are currently on in a Git repository

  :return str: name of current branch
  """
  return console.input('git rev-parse --abbrev-ref HEAD', cwd=repo_path).strip()


def status(repo_path:str) -> str:
  """
  Get current status of Git repository

  :param repo_path str: path to the target repository
  :return str: current status output
  """
  branch_name = branch(repo_path)
  s = console.input("git status", cwd=repo_path)
  new = None
  committed = None

  if 'Changes not staged for commit:' in s:
    s, new = s.split('(use "git restore <file>..." to discard changes in working directory)')
    if 'no changes added to commit (use "git add" and/or "git commit -a")' in new:
      new = new.split('no changes added to commit (use "git add" and/or "git commit -a")')[0]
    while '  ' in new:
      new = new.replace('  ', ' ')
    new = new.replace('\t', '      ').strip()
  if 'Changes to be committed:' in s:
    committed = s.split('(use "git restore --staged <file>..." to unstage)')[1]
    if 'Changes not staged for commit:' in committed:
      committed = committed.split('Changes not staged for commit:')[0]
    while '  ' in committed:
      committed = committed.replace('  ', ' ')
    committed = committed.replace('\t', '      ').strip()

  console.out(f"\n> Branch '{branch_name}' Status")
  if new is not None:
    console.out(f"  New Changes:\n      {console.out(new, 'red', False)}")
  if committed is not None:
    console.out(f"  Committed:\n      {console.out(committed, 'green', False)}")
  if new is None and committed is None:
    console.out(f"  ✅ Branch is up-to-date", "success")



def sync(repo_path:str) -> None:
  """
  This function uses the console.input method to run pull and push commands on the repository located at repo_path.
  The output of the commands is printed to the console.

  You can call this function like this: git_pull_push('/path/to/repo')
  Make sure that the repository is properly set up and that you have access to it before running this function.

  :param repo_path str: path to the target repository
  :return None:
  """
  status(repo_path)
  branch_name = branch(repo_path)
  commit_msg = f'🤖 [AUTO] {current_version} {time.timestamp()}'
  console.out(f"  {console.wait} Syncing '{branch_name}' Branch", end="\r")

  console.input('git pull -f', cwd=repo_path)
  console.input('git add .', cwd=repo_path)
  console.input(f'git commit -m "{commit_msg}"', cwd=repo_path)
  console.input('git push -f', cwd=repo_path)

  console.out(f"  ✅ Synced '{branch_name}' Branch    ", "success")
  console.out(f"     {commit_msg}", "yellow")


def checkout(repo_path:str, target:str = PRODUCTION_BRANCH, silent=False) -> None:
  """
  Sync the current branch and then switch branch from the repo_path onto the target branch

  :param repo_path str: path to the target repository
  :param target str: name of the target branch
  :return None:
  """
  branch_origin = branch(repo_path)
  console.input(f'git checkout {target}', cwd=repo_path)
  branch_destination = branch(repo_path)
  if not silent:
    console.out(
      f"\n> Switched Branch "
      f"'{console.out(branch_origin, 'yellow', False)}' -> '{console.out(branch_destination, 'green', False)}'"
    )


def merge(repo_path:str, target:str = PRODUCTION_BRANCH) -> None:
  """
  Sync the current branch, checkout target branch and then pull from the branch you were previously on.
  The out of the commands is printed to the console.

  :param repo_path str: path to the repo you wish to merge
  :param target str: name of the target branch
  :return None:
  """
  branch_name = branch(repo_path)
  #console.out(
  #  f"\n> Merge branch '{console.out(branch_name, 'green', False)}' into '{console.out(target, 'yellow', False)}'"
  #)
  sync(repo_path)
  checkout(repo_path, target, silent=True)
  console.input(f'git pull origin {branch_name}', cwd=repo_path)
  sync(repo_path)
  console.out(f"  ✅ Merged '{branch_name}' -> '{target}'", "success")
