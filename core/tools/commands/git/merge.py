from core.library import console, exists, listdir, isdir, git as GIT
from web.settings import BASE_DIR, PROJECT_NAME, LOCAL_BRANCH, STAGING_BRANCH, PRODUCTION_BRANCH, CLIENT_DATA


def check(branch_name:str):
  ''' Checks if a given branch name is designated or feature '''
  if branch_name == LOCAL_BRANCH:
    return 1
  elif branch_name == STAGING_BRANCH:
    return 2
  elif branch_name == PRODUCTION_BRANCH:
    return 3
  return 0


def check_branches_are_merge_ready():
  ''' Recursively checks all repositories current branch is logical '''
  lowest_branch_level = 9
  highest_branch_level = 0

  if exists(f"{BASE_DIR}/.git"):
    project_branch = check(GIT.branch(BASE_DIR))
    if project_branch < lowest_branch_level:
      lowest_branch_level = project_branch
    if project_branch > highest_branch_level:
      highest_branch_level = project_branch

  checked_apis = []
  api_dir = f"{BASE_DIR}/api"

  for client in CLIENT_DATA:
    source_dir = CLIENT_DATA[client]["src"]
    source_api = BASE_DIR + f'/api/{client}'

    if exists(f"{source_dir}/.git"):
      client_branch = check(GIT.branch(source_dir))
      if client_branch < lowest_branch_level:
        lowest_branch_level = client_branch
      if client_branch > highest_branch_level:
        highest_branch_level = client_branch

    if exists(f"{source_api}/.git"):
      client_api_branch = check(GIT.branch(source_api))
      if client_api_branch < lowest_branch_level:
        lowest_branch_level = client_api_branch
      if client_api_branch > highest_branch_level:
        highest_branch_level = client_api_branch

  potential_apis = listdir(api_dir)
  for dir in potential_apis:
    if (dir_path := f"{BASE_DIR}/api/{dir}") and isdir(dir_path) and (contents := listdir(dir_path)):
      if '.git' in contents and dir not in checked_apis:
        api_branch = check(GIT.branch(dir_path))
        if api_branch < lowest_branch_level:
          lowest_branch_level = api_branch
        if api_branch > highest_branch_level:
          highest_branch_level = api_branch

  if lowest_branch_level == highest_branch_level:
    return True
  return False


def merge(repo_name:str, repo_path:str):
  ''' Merges the selected repository into the next logical branch '''
  origin = GIT.branch(repo_path)
  if check(origin) == 0: dest = LOCAL_BRANCH
  elif check(origin) == 1: dest = STAGING_BRANCH
  elif check(origin) == 2: dest = PRODUCTION_BRANCH
  elif check(origin) == 3: dest = LOCAL_BRANCH
  else: return console.out(f"  [ERROR] Unexpected error while merging @ {repo_path}", "red")
  origin_label = console.out(origin, "amber", False)
  dest_label = console.out(dest, "green", False)
  console.out(f"\n> {repo_name.upper()}: merge '{origin_label}' -> '{dest_label}'", "amber")
  console.input(
    f"git branch --set-upstream-to=origin/{origin} {origin}",
    cwd=repo_path
  )
  console.input(
    f"git checkout {dest} || git checkout -b {dest}",
    cwd=repo_path,
    show_output=True
  )
  console.input(
    f"git branch --set-upstream-to=origin/{dest} {dest}",
    cwd=repo_path
  )
  console.input(
    f"git pull && git pull origin {origin} && git push origin {dest}",
    cwd=repo_path,
    show_output=True
  )


def merge_all():
  ''' Recursively merges all repositories current branch into the next logical branch '''
  console.out('')
  merge_ready = check_branches_are_merge_ready()
  if not merge_ready:
    console.out("  [ERROR] One or more branches are out of sync", "red")

  if exists(f"{BASE_DIR}/.git"):
    merge(PROJECT_NAME, BASE_DIR)

  merged_apis = []
  api_dir = f"{BASE_DIR}/api"

  for client in CLIENT_DATA:
    source_dir = CLIENT_DATA[client]["src"]
    source_api = BASE_DIR + f'/api/{client}'
    if exists(f"{source_dir}/.git"):
      merge(f"{client} (CLIENT)", source_dir)
    if exists(f"{source_api}/.git"):
      merged_apis.append(client)
      merge(f"{client} (API)", source_api)

  potential_apis = listdir(api_dir)
  for dir in potential_apis:
    if (dir_path := f"{BASE_DIR}/api/{dir}") and isdir(dir_path) and (contents := listdir(dir_path)):
      if '.git' in contents and dir not in merged_apis:
        merge(f"{dir} (API)", dir_path)


def error_message():
  return console.out("""
  `MERGE` tool takes no arguments and requires that you are on
    a designated or feature branch and will merge your current
    branch into the next logical designated branch.

    FEATURE_BRANCH -> into -> LOCAL_BRANCH
    LOCAL_BRANCH -> into -> STAGING BRANCH
    STAGING_BRANCH -> into -> PRODUCTION_BRANCH
    PRODUCTION_BRANCH -> into -> LOCAL_BRANCH

    Any branch which is not listed as a designated branch will
    be assumed as a feature branch while using the merge tool.

    ./o merge""",
    "red"
  )
