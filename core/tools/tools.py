# Standard library
import readline
import subprocess
from os.path import exists
from os import system, getcwd, environ, mkdir
from sys import argv, path, executable, version_info
# Overlord library
from web.settings import *
from core import create_user
from core.library import execute_from_command_line, console, git as GIT, url
from core.library.version import Version
from core.tools.library import gracefulExit, updater
from core.tools.commands import install, git, django, node, pytest, pa, vscode, fs, nginx, server, redis

tools_path = '/'.join(__file__.split('/')[:-1])
project_path = path[0]
command_line = argv[2:]
_version = Version()
environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')


def awaitInput(ascii_art=True):
  global command_line

  if ascii_art:
    print(f'''
  -------------------------------------------------------------------

   ██████╗ ██╗   ██╗███████╗██████╗ ██╗      ██████╗ ██████╗ ██████╗
  ██╔═══██╗██║   ██║██╔════╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
  ██║   ██║██║   ██║█████╗  ██████╔╝██║     ██║   ██║██████╔╝██║  ██║
  ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██║     ██║   ██║██╔══██╗██║  ██║
  ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████╗╚██████╔╝██║  ██║██████╔╝
   ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝
                               Ver {_version.major}.{_version.minor}.{_version.patch}
                         {git.check.version_status_label()}
          To get help & information read the documentation here
                  https://www.easter.company/overlord

  -------------------------------------------------------------------''')

  # Check for updates
  update_status = updater.check_status()
  if update_status[0]:
    console.out(f"                 Update Available {update_status[1]}", "yellow")

  # Initialize Clients
  for _client in node.clients.load_clients_json():
    node.clients.initialize(_client)

  # Initialize Database
  if not exists(f'{BASE_DIR}/db.sqlite3'):
    console.out("\n> Creating Database & Making Migrations\n")
    django.server.migrate_database()

  # Initialize Static Directories
  print('')
  for _dir in STATICFILES_DIRS:
    if not exists(_dir):
      try:
        mkdir(_dir)
      except Exception as static_directory_creation_error:
        console.out(
          f"    failed to create static files directory {_dir}\n{static_directory_creation_error}",
          "yellow"
        )

  # Initialize Console Interface
  readline.clear_history()
  flag = gracefulExit.GracefulExit()

  while True:
    try:
      Input = input(console.out('./o ', 'green', False)).strip()
      while '  ' in Input:
        Input = Input.replace('  ', ' ')
      command_line = Input.split(' ')
      run()
    except EOFError:
      console.out("\n\nAre you trying to exit the CLI? (Please use the 'exit' command instead)\n", "yellow")
    if flag.exit():
      break


def output(line, error=False, success=False, warning=False):
  _output = "\n"

  if error:
    _output += " [ERROR] "
  elif warning:
    _output += " [WARNING] "

  if callable(line):
    _output += f'{line()}\n'
  else:
    _output += f'{line}\n'

  if error:
    return console.out(_output, 'red')
  elif warning:
    return console.out(_output, 'yellow')
  elif success:
    return console.out(_output, 'green')
  return console.out(_output)


def help():
  return print(f'''
  {console.out("Welcome to Overlord.", "blue", False)}
  The help command lists the 10 most common commands within Overlord-CLI

  01. clear
    - Clears the terminal window of any input/output allowing you to
      free up space on your screen.

  02. clients
    - Lists all the clients in your clients directory that are either
      installed or ready-to-install.

  03. code
    - Opens vscode in the root directory of your current project.
    - Takes 1 optional argument `-<client_name>` which opens a client
      and it's associated API in an isolated workspace.
    - Only works for vscode stable release channel, not insiders.
      (unless you use an alias)

  04. exit
    - Close the Overlord-CLI and stop running any background threads
      for clients & servers.

  05. pull
    - Automatically detect all git repositories within this projects
      scope and pull latest commits from the current branch.

  06. push
    - Automatically detect all git repositories within this projects
      scope and push the latest commits to the current branch.

  07. merge
    - Automatically merges your current branch into the next logical
      branch for your projects flow.
    - Set `LOCAL_BRANCH`, `STAGING_BRANCH` & `PRODUCTION_BRANCH`
      branch names for your project inside your server.json
      configuration file.

  08. branch
    - If no arguments are passed it prints the current branch
      of each API & Client within your project.
    - Pass a single argument `-<branch_name>` to recursively
      switch the branch of each API & Client within your project

  09. create
    - Used to create a new web based or multi-platform client.
    - Run the command with no arguments to receive detailed usage
      instructions

  10. share
    - Used to share an Asset, Component or Library from one client
      with another client inside this project.
    - Run the command with no arguments to receive detailed usage
      instructions

    Detailed and up-to-date documentation is kept on our website
                {console.out("https://www.easter.company/overlord", "blue", False)}'''
  )


def run_tool(command, index=0):
  # General input variables
  arguments_remaining = 0
  arguments = []

  # Clear log cache
  console.clear_log_cache()

  # Collect arguments and count them
  for arg in command_line[index + 1:]:
    if arg.startswith('-'):
      arguments_remaining += 1
      arguments.append('-'.join(arg.split('-')[1:]))
    else:
      break

  # Return an error prompt if the command string is an argument
  if command.startswith('-') and index == 0:
    console.out("\n  [ERROR] Commands cannot start with '-'", "red")

  elif command.startswith('-') or command == '':
    return None

  elif command == 'install':

    # Install python requirements
    if arguments_remaining > 0 and ('r' in arguments or 'd' in arguments):
      if arguments_remaining > 0 and 'r' in arguments:
        django.server.install_requirements()
      if arguments_remaining > 0  and 'd' in arguments:
        django.server.install_requirements_dev()

    # Install all clients
    elif arguments_remaining == 1 and (arguments[0] == 'clients' or arguments[0] == 'all'):
      node.clients.install()

    # Install a specific client
    elif arguments_remaining > 0:
      for argument in arguments:
        node.clients.install(argument)

    # Install Overlord
    else:
      # System Overwrite Warning
      if exists('./db.sqlite3'):
        output(
          "You are about to overwrite your current installation.\n"
          "This will cause you to lose access to all your encrypted data.\n"
        )
        _input = input('Type "confirm" to continue anyway: ')
        if not _input.lower() == "confirm":
          return output("User did not confirm to a system overwrite.")
      django.server.install_requirements()
      install.make_server_config()
      install.django_files()
      install.make_secrets_file()
      install.o_file()
      install.setup_cfg()
      django.secret_key.new()
      console.out('\nSuccessfully Installed!', 'success')
      console.out(f'Enter {console.out("./o", "yellow", False)} to begin using Overlord.')

  elif command == 'pull':
    git.pull.all()

  elif command == 'push':
    git.push.all()

  elif command == 'merge':
    if arguments_remaining == 0:
      git.merge.merge_all()
    else:
      git.merge.error_message()

  elif command == 'branch':
    if not exists(f"{BASE_DIR}/.git"):
      console.out(f"\nProject is not contained within a repository", "red")
    if arguments_remaining == 1:
      target_branch = arguments[0].title() if arguments[0].title() in [
          LOCAL_BRANCH, STAGING_BRANCH, PRODUCTION_BRANCH
      ] else arguments[0]
      git.branch.switch_all(target_branch)
    else:
      console.out(f"\nLocal: {console.out(LOCAL_BRANCH, 'amber', False)}")
      console.out(f"Staging: {console.out(STAGING_BRANCH, 'amber', False)}")
      console.out(f"Production: {console.out(PRODUCTION_BRANCH, 'green', False)}")
      git.branch.list_all()

  elif command == 'new_secret_key':
    django.secret_key.new()

  elif command == 'test':
    pytest.run.all_tests()

  elif command == 'runclient' or command == 'run':

    if arguments_remaining == 1 and arguments[0] == 'all':
      node.clients.run_all(none_on_main_thread=True)
      django.server.start()
      node.share.file_updater_thread()

    elif arguments_remaining >= 1:
      any_valid_client = False
      already_started = False
      for arg in arguments:
        if arg in CLIENT_DATA:
          if 'npx expo' in CLIENT_DATA[arg]['start']:
            already_started = True
            django.server.start()
            node.share.file_updater_thread()
            node.clients.run(arg, False, False)
          else:
            any_valid_client = True
            node.clients.run(arg, False, True)
      if any_valid_client and not already_started:
        django.server.start()
        node.share.file_updater_thread()

    elif command == 'run':
      if INDEX is not None and INDEX != '':
        node.share.file_updater_thread()
        node.clients.run(INDEX, False, True)
        django.server.start()
      else:
        console.out(
          "\n  [ERROR] `run` command requires a client to be set as your `INDEX`"
          "\n          from within your .config/server.json configuration file. ",
          "red"
        )

  elif command == 'runserver':
    console.out("\nStarting Production Server", "green")
    console.out("[Press CTRL+C to Return]\n")
    django.server.run()

  elif command == 'build':
    if arguments_remaining < 1:
      return node.clients.error_message()
    if arguments_remaining == 1 and arguments[0] == 'all':
      node.clients.build_all()
    else:
      for arg in arguments:
        node.clients.build(arg)
    return print()

  elif command == 'migrate':
    django.server.migrate_database()

  elif command == 'collectstatic':
    django.server.collect_staticfs()

  elif command == 'start':
    if pytest.run.all_tests():
      node.clients.build_all()
      django.server.start()
    else:
      exit("One or more unit tests failed")

  elif command == 'server' and len(SECRET_DATA['PA_USER_ID']) > 0 and len(SECRET_DATA['PA_API_KEY']) > 0:
    if arguments_remaining == 1:
      if arguments[0] == 'apps':
        return pa.apps.display()
      elif arguments[0] == 'consoles':
        return pa.consoles.display()
      elif arguments[0] == 'cpu':
        return pa.cpu.display()
      elif arguments[0] == 'tasks':
        return pa.tasks.display()
      elif arguments[0] == 'reload':
        pa.reload.request()
        return print()
      elif arguments[0] == 'status':
        pa.status.request()
        return print()
      elif arguments[0] == 'upgrade':
        pa.upgrade.request()
        return print()
      elif arguments[0] == 'deploy':
        cur_branch = GIT.branch(BASE_DIR)
        if cur_branch == STAGING_BRANCH or cur_branch == PRODUCTION_BRANCH:
          if cur_branch == STAGING_BRANCH:
            system('clear')
            console.out(f"\n======== Building All Clients ========", "yellow")
            node.clients.build_all()
            console.out(f"\n========= Sync API & Clients =========", "yellow")
            GIT.sync_all_clients()
            console.out(f"\n======== Merging `{PRODUCTION_BRANCH}` Branch ========", "yellow")
            GIT.merge(BASE_DIR, PRODUCTION_BRANCH)
            GIT.checkout(BASE_DIR, LOCAL_BRANCH)
            GIT.sync_local_with_production(BASE_DIR)
            console.out(f"\n======= Deploy {_version} to Server =======", "yellow")
          pa.upgrade.request()
          pa.reload.request()
          pa.status.request()
          return print()
        else:
          console.out(
            f"\n  [ERROR] You can only deploy from the `{STAGING_BRANCH}` or `{PRODUCTION_BRANCH}` branch",
            "red"
          )
    else:
      return pa.api.error_message()

  elif command.startswith('server'):
    if command.startswith('server:server'):
      server.no_server_cmd_error_message()
    elif command.startswith('server:') and len(SECRET_DATA['SERVER_URL']) > 0:
      server_cmd = command.replace('server:', '', 1)
      server.post_command(server_cmd, arguments)
    else:
      server.error_message()

  elif command == 'reload':
    if arguments_remaining == 1 and arguments[0] == 'nginx':
      console.sudo(f"systemctl reload nginx", show_output=True)
    else:
      if not exists(f"/etc/systemd/system/{PROJECT_NAME}.service"):
        console.out(f"  {console.failure} '{PROJECT_NAME}.service' doesn't exist.")
      else:
        console.sudo(f"systemctl restart {PROJECT_NAME}", show_output=True)

  elif command == 'create':
    # Universal API
    if arguments_remaining >= 1 and arguments[0] == 'api':
      if arguments_remaining == 3 and (arguments[1].startswith('https://') or arguments[1].startswith('git@')):
        django.api.create(arguments[2], arguments[1])
      elif arguments_remaining == 2 and (arguments[1].startswith('https://') or arguments[1].startswith('git@')):
        new_api_name = arguments[1].split('/')[-1].split('.git')[0].lower()
        django.api.create(new_api_name, arguments[1])
      elif arguments_remaining == 2:
        django.api.create(arguments[1])
      else:
        node.clients.create_cmd_error_message()
    # Custom client
    elif arguments_remaining == 1 and (arguments[0].startswith('https://') or arguments[0].startswith('git@')):
      new_client_name = arguments[0].split('/')[-1].split('.git')[0].lower()
      node.clients.create(new_client_name, custom_repo=arguments[0])
    # Default web client
    elif arguments_remaining == 1:
      node.clients.create(arguments[0].lower())
    # Default native client
    elif arguments_remaining == 2 and arguments[0] == 'native':
      node.clients.create(arguments[1].lower(), native=True)
    # Custom client with `name` argument
    elif arguments_remaining == 2 and (arguments[0].startswith('https://') or arguments[0].startswith('git@')):
      node.clients.create(arguments[1].lower(), custom_repo=arguments[0])
    # Invalid input error
    else:
      node.clients.create_cmd_error_message()
    # Acquire associated APIs for any new clients
    client_data = install.make_clients_config(BASE_DIR)
    statements = url.acquire_all_apis(client_data, BASE_DIR, no_tab=True)
    url.write_api_urls(statements, BASE_DIR)
    url.write_api_models(statements, BASE_DIR)

  elif command == 'remove':
    if arguments_remaining == 1:
      return node.clients.remove(arguments[0])
    else:
      return node.clients.remove_cmd_error_message()

  elif command == 'share':
    if arguments_remaining == 2:
      node.share.target(arguments[0], arguments[1])
    else:
      node.share.error_message()

  elif command == 'help': help()

  elif command == 'clients':
    for _client in node.clients.load_clients_json():
      console.out(f'\n -> {_client}', 'yellow')

  elif command == 'cwd': output(getcwd)

  elif command == 'size':
    dir_path = getcwd()
    _process = subprocess.run(['du', '-sh', dir_path], capture_output=True, text=True)
    dir_size = _process.stdout.split()[0] + 'B'
    console.out('\n' + dir_size)

  elif command == 'node':
    if not arguments_remaining == 0:
      return output(
        "`node` command doesn't take any arguments",
        error=True
      )
    console.out('\nStarting Node Shell', 'green')
    console.out('[Press CTRL+D to Return]')
    system('node')
    console.out('\nClosed Node.', 'red')

  elif command == 'django' or command == 'python':
    if not arguments_remaining == 0:
      return output(
        "`django` command doesn't take any arguments",
        error=True
      )
    console.out('\nStarting Python-Django Shell', 'green')
    console.out('[Press CTRL+D to Return]')
    execute_from_command_line([executable, 'shell_plus'])
    console.out('\nClosed Python-Django Shell.', 'red')

  elif command == 'redis':
    if arguments_remaining == 1 and arguments[0] == 'setup':
      redis.setup.run()
    if arguments_remaining == 1 and arguments[0] == 'test':
      redis.test.run()
    else:
      redis.error_message()

  elif command.startswith('npm') and arguments_remaining > 0:
    if arguments[0] == 'uninstall' or arguments[0] == 'u':
      [ node.npm.install(arguments[1], package, True) for package in arguments[2:] ]
    elif arguments[0] == 'install' or arguments[0] == 'i':
      [ node.npm.install(arguments[1], package, False) for package in arguments[2:] ]
    elif command == 'npm-uninstall':
      [ node.npm.install(arguments[0], package, True) for package in arguments[1:] ]
    elif command == 'npm' or command == 'npm-install':
      [ node.npm.install(arguments[0], package, False) for package in arguments[1:] ]

  elif command == 'status':
    if arguments_remaining == 0:
      GIT.status(BASE_DIR)
    else:
      for _arg in arguments:
        git.status.clients(_arg)

  elif command == 'clear':
    system('clear')

  elif command == 'code':
    if arguments_remaining == 0:
      console.out("\n> opening global workspace")
      console.input('code .')
    elif arguments_remaining == 1 and arguments[0] in CLIENT_DATA:
      console.out(f"\n> opening workspace for '{arguments[0]}'")
      if 'api' in CLIENT_DATA[arguments[0]]:
        vscode.workspace.start(arguments[0])
      else:
        console.input(f'code clients/{arguments[0]}')
      return print('')
    else:
      return console.out("\n  [ERROR] `code` command takes 1 argument that must be a client name\n", "red")

  elif command == 'sh':
    if arguments_remaining > 0:
      console.out("\n> Execute shell command", "yellow")
      console.input(' '.join(arguments), show_output=True)
    else:
      sh_input = input("\n> ")
      console.input(sh_input, show_output=True)

  elif command == 'exit' or command == 'exit()':
    console.out("\nClosed Overlord-CLI\n", "red")
    exit()

  elif command == 'createsuperuser' or command == 'createadmin':
    create_user(99)

  elif command == 'createuser':
    create_user(1)

  elif command == 'update':
    update_status = updater.check_status(force=True)
    if update_status[0]:
      console.out(f"\n> Updating Overlord {update_status[1]}")
      updater.clone_latest_version()
    else:
      console.out(f"\n> {update_status[1]}")

  elif command == 'ls':
    if arguments_remaining == 0:
      fs.ls.ls_project()
    else:
      fs.ls.ls_project(arguments)

  elif command == 'nginx':
    if arguments_remaining == 0:
      nginx.error_message()
    elif arguments_remaining == 1:
      if arguments[0] == 'setup':
        nginx.setup.run()
      elif arguments[0] == 'start':
        nginx.service.start()
      elif arguments[0] == 'stop':
        nginx.service.stop()
      elif arguments[0] == 'restart':
        nginx.service.restart()

  else:
    line_start = "\n" if index == 0 else ""
    console.out(f"{line_start}  [ERROR] No command matching input\n    ./o {command}", "red")

  return print('')


def run(set_command_line:str|None = None):
  global command_line
  if not version_info >= (3, 10):
    console.out(
      "\n[ERROR] Python 3.10 or greater is required by Overlord\n"
      "        You may have installed using the wrong executable\n"
      "        Try installing Overlord again using this command\n"
      "        from within your projects directory:\n"
      "        \n"
      "        >> python3.10 core.py tools install\n"
      "        \n"
      "        or set python 3.10 (or greater) to be your system default\n"
      "        when calling 'python3' from the command line.\n",
      "red"
    ), exit()
  elif set_command_line is not None:
    command_line = set_command_line
    [run_tool(command, index) if not command == './o' else None for index, command in enumerate(set_command_line)]
  elif len(command_line) <= 0:
    awaitInput()
  else:
    [run_tool(arg, index) if not arg == './o' else None for index, arg in enumerate(command_line)]
