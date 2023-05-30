from core.library import console, exists, listdir, isdir, git as GIT
from web.settings import BASE_DIR, PROJECT_NAME, CLIENT_DATA, LOCAL_BRANCH, STAGING_BRANCH, PRODUCTION_BRANCH


def switch(target:str, repo_name:str, repo_path:str) -> str:
  ''' Create if not exists and checkout a repository at the target branch '''
  origin = GIT.branch(repo_path)
  console.input(f"git checkout {target} || git checkout -b {target}", cwd=repo_path)
  if GIT.branch(repo_path) == target:
    return console.out(
      f"> {repo_name.upper()}: branch "
      f"'{console.out(origin, 'yellow', False)}' -> '{console.out(target, 'green', False)}'"
    )
  return console.out(
    f"> {repo_name.upper()} "
    f"failed to checkout @ {target}"
  )


def switch_all(target:str) -> str:
  ''' Recursively switches all repositories within the project to a designated branch '''
  print('')

  designated_branches = [ LOCAL_BRANCH, STAGING_BRANCH, PRODUCTION_BRANCH ]
  if target not in designated_branches:
    return console.out("  [ERROR] Target branch is not a designated branch", "red")

  if exists(f"{BASE_DIR}/.git"):
    switch(target, PROJECT_NAME, BASE_DIR)
  switched_apis = []
  api_dir = f"{BASE_DIR}/api"

  for client in CLIENT_DATA:
    source_dir = CLIENT_DATA[client]["src"]
    source_api = BASE_DIR + f'/api/{client}'

    if exists(f"{source_dir}/.git"):
      switch(target, f"{client} (CLIENT)", source_dir)

    if exists(f"{source_api}/.git"):
      switched_apis.append(client)
      switch(target, f"{client} (API)", source_api)

  potential_apis = listdir(api_dir)
  for dir in potential_apis:
    if (dir_path := f"{BASE_DIR}/api/{dir}") and isdir(dir_path) and (contents := listdir(dir_path)):
      if '.git' in contents and dir not in switched_apis:
        switch(target, f"{dir} (API)", dir_path)

  return target


def list_all() -> None:
  ''' Recursively print the current branch for all repositories within the project '''
  print('')

  if exists(f"{BASE_DIR}/.git"):
    cur_branch = GIT.branch(BASE_DIR)
    if cur_branch == PRODUCTION_BRANCH:
      cur_branch_col = "green"
    elif cur_branch == STAGING_BRANCH:
      cur_branch_col = "amber"
    elif cur_branch == LOCAL_BRANCH:
      cur_branch_col = "red"
    else:
      cur_branch_col = "blue"
    cur_branch = console.out(cur_branch, cur_branch_col, False)
    console.out(f"{PROJECT_NAME.upper()}: {cur_branch}")

  printed_apis = []
  api_dir = f"{BASE_DIR}/api"

  for client in CLIENT_DATA:
    source_dir = CLIENT_DATA[client]["src"]
    source_api = BASE_DIR + f'/api/{client}'

    if exists(f"{source_dir}/.git"):
      cur_branch = GIT.branch(source_dir)
      if cur_branch == PRODUCTION_BRANCH:
        cur_branch_col = "green"
      elif cur_branch == STAGING_BRANCH:
        cur_branch_col = "amber"
      elif cur_branch == LOCAL_BRANCH:
        cur_branch_col = "red"
      else:
        cur_branch_col = "blue"
      cur_branch = console.out(cur_branch, cur_branch_col, False)
      console.out(f"{client.upper()} (CLIENT): {cur_branch}")

    if exists(f"{source_api}/.git"):
      printed_apis.append(client)
      cur_branch = GIT.branch(source_api)
      if cur_branch == PRODUCTION_BRANCH:
        cur_branch_col = "green"
      elif cur_branch == STAGING_BRANCH:
        cur_branch_col = "amber"
      elif cur_branch == LOCAL_BRANCH:
        cur_branch_col = "red"
      else:
        cur_branch_col = "blue"
      cur_branch = console.out(cur_branch, cur_branch_col, False)
      console.out(f"{client.upper()} (API): {cur_branch}")

  potential_apis = listdir(api_dir)
  for dir in potential_apis:
    if (dir_path := f"{BASE_DIR}/api/{dir}") and isdir(dir_path) and (contents := listdir(dir_path)):
      if '.git' in contents and dir not in printed_apis:
        cur_branch = GIT.branch(dir_path)
        if cur_branch == PRODUCTION_BRANCH:
          cur_branch_col = "green"
        elif cur_branch == STAGING_BRANCH:
          cur_branch_col = "amber"
        elif cur_branch == LOCAL_BRANCH:
          cur_branch_col = "red"
        else:
          cur_branch_col = "blue"
        cur_branch = console.out(cur_branch, cur_branch_col, False)
        console.out(f"{dir.upper()} (API): {cur_branch}")
