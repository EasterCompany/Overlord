# Standard library
import readline
import subprocess
from os.path import exists
from os import system, getcwd, environ
from sys import argv, path, executable, version_info
# Overlord library
from web.settings import *
from core import create_user, create_super_user
from core.library import execute_from_command_line, console, git as GIT
from core.library.version import Version
from core.tools.library import gracefulExit
from core.tools.commands import install, git, django, node, pytest, pa, vscode

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

    -------------------------------------------------------------------
        ''')
    else:
        print('')

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
    Welcome to Overlord.

    This command is here to help you get started with the basics.
    To begin with lets go over some simple developer commands that'll
    help make your experience here simple and easy.

    01. clients
        - Lists all the clients in your clients directory that are either
          installed or ready-to-install.

    02. clear
        - Clears the terminal window of any input/output allowing you to
          free up space on your screen.

    03. code
        - Opens vscode in the root directory of your current project.
        - Takes 1 optional argument "client_name" which opens a client
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

    07. main                                      {console.out("[Experimental Feature]", "yellow", False)}
        - Automatically detect all git repositories within this projects
          scope and switch them to the `main` branch.

    08. dev                                       {console.out("[Experimental Feature]", "yellow", False)}
        - Automatically detect all git repositories within this projects
          scope and switch them to the `dev` branch.

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

    # Collect arguments and count them
    for arg in command_line[index + 1:]:
        if arg.startswith('-'):
            arguments_remaining += 1
            arguments.append('-'.join(arg.split('-')[1:]))
        else:
            break

    # Used for commit, merge & deploy commands
    if arguments_remaining >= 2:
        git_repo = ''.join(
            command_line[index + 1].split('-')[1:]
        )
        git_message = ''.join(
            ' '.join(command_line[index + 2:]).split('-')[1:]
        )
    else:
        git_repo, git_message = None, None

    # Return an error prompt if the command string is an argument
    if command.startswith('-') and index == 0:
        console.out("\n  [ERROR] Commands cannot start with '-'", "red")

    elif command.startswith('-'):
        return None

    elif command == 'install':

        # Install python requirements
        if arguments[0] == 'r' or arguments[0] == 'requirements':
            django.server.install_requirements()
            # Include developer dependencies
            if arguments[1] == 'd':
                django.server.install_requirements_dev()

        # Install all clients
        elif arguments_remaining == 1 and (arguments[0] == 'clients' or arguments[0] == 'all'):
            print("\nInstalling all clients:")
            node.clients.install()

        # Install a specific client
        elif arguments_remaining > 0:
            for argument in arguments:
                print(f"\nInstalling client: {argument}")
                print("---------------------------------------------")
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
            # Install Overlord Dependencies
            output('Installing requirements.txt...')
            system(f'{executable} -m pip install -r requirements.txt')
            output('\nInstalling Overlord-Tools...')
            git.pull.branch_origins('dev', None)
            git.pull.branch_origins('main', None)
            print(' ')
            # Install Overlord Configurations
            install.make_server_config(project_path)
            install.django_files(project_path)
            install.secrets_file(project_path)
            install.o_file(project_path)
            install.pytest_ini(project_path)
            django.secret_key.new(project_path)
            console.out('\nSuccess!\n', 'green')

    elif command == 'pull':
        git.pull.all()

    elif command == 'push':
        git.push.all()

    elif command == 'merge':
        if arguments_remaining == 0:
            cur_branch = GIT.branch(BASE_DIR)
            if cur_branch == LOCAL_BRANCH:
                GIT.merge(BASE_DIR, target=STAGING_BRANCH)
            elif cur_branch == STAGING_BRANCH:
                GIT.merge(BASE_DIR, target=PRODUCTION_BRANCH)
            elif cur_branch == PRODUCTION_BRANCH:
                console.out("\n  [ERROR] Cannot merge Production Branch", "red")
        else:
            console.out("\n  [ERROR] `merge` command does not take any arguments", "red")

    elif command == 'branch':
        if arguments_remaining == 1:
            target_branch = arguments[0].title() if arguments[0].title() in [
                LOCAL_BRANCH, STAGING_BRANCH, PRODUCTION_BRANCH
            ] else arguments[0]
            GIT.checkout(BASE_DIR, target_branch)
        else:
            cur_branch = GIT.branch(BASE_DIR)
            console.out(f"\nCurrent: {console.out(cur_branch, 'green', False)}")
            console.out(f"\nEnvironments ----\n  Local: {console.out(LOCAL_BRANCH, 'yellow', False)}")
            console.out(f"  Staging: {console.out(STAGING_BRANCH, 'yellow', False)}")
            console.out(f"  Production: {console.out(PRODUCTION_BRANCH, 'yellow', False)}")

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
            for arg in arguments:
                if arg in CLIENT_DATA:
                    any_valid_client = True
                node.clients.run(arg, False, True)
            if any_valid_client:
                django.server.start()
                node.share.file_updater_thread()

        elif command == 'run':
            node.clients.run(INDEX, False, True)
            django.server.start()
            node.share.file_updater_thread()

        return awaitInput(False)

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
            gracefulExit(99)

    elif command == 'server':

        if arguments_remaining == 1:

            if arguments[0] == 'apps':
                pa.apps.display()
                return print()
            elif arguments[0] == 'consoles':
                pa.consoles.display()
                return print()
            elif arguments[0] == 'cpu':
                pa.cpu.display()
                return print()
            elif arguments[0] == 'tasks':
                pa.tasks.display()
                return print()
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
                        node.clients.build_all()
                        GIT.merge(BASE_DIR, PRODUCTION_BRANCH)
                        console.out(f"\n> Syncing & Resetting `{LOCAL_BRANCH}` Branch", "blue")
                        GIT.merge(BASE_DIR, LOCAL_BRANCH)
                        console.out(f"\n> Deploying v{_version} to Production Server", "blue")
                    pa.upgrade.request()
                    pa.reload.request()
                    pa.status.request()
                    return print()
                else:
                    console.out(
                        f"\n  [ERROR] You can only deploy from the `{STAGING_BRANCH}` branch", "red"
                    )
        else:
            return pa.api.error_message()

    elif command == 'create':
        # Custom client
        if arguments_remaining == 1 and (arguments[0].startswith('https://') or arguments[0].startswith('git@')):
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
            node.clients.error_message()

    elif command == 'share':
        if arguments_remaining == 2:
            node.share.target(arguments[0], arguments[1])
        else:
            node.share.error_message()

    elif command == 'help': help()

    elif command == 'clients':
        for _client in node.clients.update_client_json():
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
        output(console.out('\nInitiating Redis Cloud Connection', 'green', False) + ' \n[CTRL+C to Exit]')
        system(
            f"redis-cli -u redis://{SECRET_DATA['REDIS-USER']}:{SECRET_DATA['REDIS-PASS']}@{SECRET_DATA['REDIS-HTTP']}"
        )
        console.out('Closed Redis Cloud Connection.', 'red')

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
        _process = subprocess.run(arguments, capture_output=True, text=True)
        console.out('\n' + _process.stdout)

    elif command == 'exit' or command == 'exit()':
        console.out("\nClosed Overlord-CLI\n", "red")
        exit()

    elif command == 'createsuperuser' or command == 'createadmin':
        create_super_user()

    elif command == 'createuser':
        create_user()

    else:
        line_start = "\n" if index == 0 else ""
        console.out(f"{line_start}  [ERROR] No command matching input\n    ./o {command}", "red")

    return print('')


def run():
    if not version_info >= (3, 10):
        return console.out(
            "\n[ERROR] Python 3.10 or greater is required by Overlord\n"
            "        You may have installed using the wrong executable\n"
            "        Try installing Overlord again using this command:\n"
            "        \n"
            "        python3.10 core.py tools install\n"
            "        \n"
            "        or set python 3.10 (or greater) to be your system default\n"
            "        when calling 'python3' from the command line.\n",
            "red"
        ), exit()
    if len(command_line) <= 0:
        return awaitInput()
    [run_tool(arg, index) for index, arg in enumerate(command_line)]
