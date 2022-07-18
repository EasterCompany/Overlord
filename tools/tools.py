# Standard library
import subprocess
from os import system, getcwd
from sys import argv, path, executable

# Overlord library
from core.library.version import Version
from tools.library import console, gracefulExit
from tools.commands import install, git, django, node, pytest, pa

tools_path = '/'.join(__file__.split('/')[:-1])
project_path = path[0]
command_line = argv[2:]
len_cmd_line = len(command_line)
_version = Version()


def awaitInput(ascii_art=True):
    global command_line

    if ascii_art:
        print(f'''    -------------------------------------------------------------------

     ██████╗ ██╗   ██╗███████╗██████╗ ██╗      ██████╗ ██████╗ ██████╗
    ██╔═══██╗██║   ██║██╔════╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
    ██║   ██║██║   ██║█████╗  ██████╔╝██║     ██║   ██║██████╔╝██║  ██║
    ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██║     ██║   ██║██╔══██╗██║  ██║
    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████╗╚██████╔╝██║  ██║██████╔╝
     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝
                              Ver {_version.major}.{_version.minor}.{_version.patch}

    To get help & information about the Overlord-CLI go to this github
    address or read your local README.md.

    https://github.com/EasterCompany/Overlord/blob/main/README.md

    -------------------------------------------------------------------
        ''')
    else:
        print('')

    flag = gracefulExit.GracefulExit()
    while True:
        Input = input(console.col('./o ', 'green'))
        command_line = Input.split(' ')
        run()
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
        return print(console.col(_output, 'red'))
    elif warning:
        return print(console.col(_output, 'yellow'))
    elif success:
        return print(console.col(_output, 'green'))
    return print(_output)


def help():
    return print('''
    Welcome to Overlord.

    This command is here to help you get started with the basics.
    To begin with lets go over some simple developer commands that'll
    help make your experience here - fast and easy.

    01. clients
        - Lists all the clients in your clients directory that are either
          installed or ready-to-install.

    02. clear
        - Clears the terminal window of any input/output allowing you to
          free up space on your screen.

    03. code
        - Opens vscode in the root directory of your current project.
        - Only works for vscode stable release channel, not insiders.
        - "code ." command must also work on your environment.

    04. exit
        - Close the Overlord-CLI and stop running any background threads
          for clients & servers.

    05. pull
        - Automatically detect all git repositories within this projects
          scope and pull latest commits from the current branch.

    06. push
        - Automatically detect all git repositories within this projects
          scope and push the latest commits to the current branch.

    07. main
        - Automatically detect all git repositories within this projects
          scope and switch them to the `main` branch.

    08. dev
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

    Detailed and up-to-date documentation is kept on our GitHub Repo
    Read this for more [https://github.com/EasterCompany/Overlord#readme]
    ''')


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
    if command.startswith('-'): return None

    elif command == 'install':
        # Install a specific or various Overlord Clients
        if arguments_remaining == 1 and (arguments[0] == 'clients' or arguments[0] == 'all'):
            print("\n Installing all clients:")
            return node.clients.install()

        elif arguments_remaining > 0:
            for argument in arguments:
                print(f"\n Installing client: {argument}")
                print(" ----------------------------------- ")
                node.clients.install(argument)
            return

        # Install Overlord Server
        output('\nInstalling Overlord-Tools...')
        git.update.all()

        def set_branch_origins(repo=None):
            git.update.branch_origins('dev', repo)
            git.update.branch_origins('main', repo)

        set_branch_origins()
        print(' ')
        install.make_server_config(project_path)
        install.django_files(project_path)
        install.secrets_file(project_path)
        print('\n', console.col('Success!.', 'green'), '\n')

    elif command == 'pull':
        system('./o pull')

    elif command == 'push':
        system('./o push')

    elif command == 'dev' or command == 'development':
        git.branch.switch('dev')

    elif command == 'main' or command == 'production':
        git.branch.switch('main')

    elif command == 'merge':
        if arguments_remaining == 2:
            if arguments[0] == 'all': git.merge.all(git_message), gracefulExit()
            else: git.merge.with_message(git_message, git_repo), gracefulExit()
        git.merge.error_message(), gracefulExit()

    elif command == 'new_secret_key':
        django.secret_key.new()

    elif command == 'test':
        pytest.run.all_tests()

    elif command == 'runclient' or command == 'run':

        if arguments_remaining < 1 and not command == 'run':
            return node.clients.error_message()

        elif arguments_remaining == 1 and arguments[0] == 'all':
            node.clients.run_all()

        elif arguments_remaining >= 1:
            for arg in arguments:
                node.clients.run(arg, False, True)

        elif command == 'run':
            node.clients.run_all(none_on_main_thread=True)

        django.server.start()

        return node.share.file_updater_thread()

    elif command == 'runserver':
        django.server.run()

    elif command == 'build':
        if arguments_remaining < 1:
            return node.clients.error_message()
        if arguments_remaining == 1 and arguments[0] == 'all':
            return node.clients.build_all()
        else:
            for arg in arguments:
                node.clients.build(arg)
        return django.server.collect_staticfs()

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
                return pa.apps.display()
            elif arguments[0] == 'consoles':
                return pa.consoles.display()
            elif arguments[0] == 'cpu':
                return pa.cpu.display()
            elif arguments[0] == 'tasks':
                return pa.tasks.display()
            elif arguments[0] == 'reload':
                return pa.reload.request()
            elif arguments[0] == 'status':
                return pa.status.request()
            elif arguments[0] == 'upgrade':
                pa.upgrade.request()
                pa.reload.request()
                return pa.status.request()

        else:
            return pa.api.error_message()

    elif command == 'create':
        # Custom client
        if arguments_remaining == 1 and (arguments[0].startswith('https://') or arguments[0].startswith('git@')):
            new_client_name = arguments[0].split('/')[-1].split('.git')[0].lower()
            return node.clients.create(new_client_name, custom_repo=arguments[0])
        # Default web client
        elif arguments_remaining == 1:
            return node.clients.create(arguments[0].lower())
        # Default native client
        elif arguments_remaining == 2 and arguments[0] == 'native':
            return node.clients.create(arguments[1].lower(), native=True)
        # Custom client with `name` argument
        elif arguments_remaining == 2 and (arguments[0].startswith('https://') or arguments[0].startswith('git@')):
            return node.clients.create(arguments[1].lower(), custom_repo=arguments[0])
        # Invalid input error
        else:
            return node.clients.error_message()

    elif command == 'share':
        if arguments_remaining == 2:
            return node.share.target(arguments[0], arguments[1])
        else:
            return node.share.error_message()

    elif command == 'help': help()

    elif command == 'clients':
        for _client in node.clients.update_client_json():
            output(f' -> {_client}')

    elif command == 'cwd': output(getcwd)

    elif command == 'size':
        dir_path = getcwd()
        _process = subprocess.run(['du', '-sh', dir_path], capture_output=True, text=True)
        dir_size = _process.stdout.split()[0] + 'B'
        output(dir_size)

    elif command == 'node':
        if not arguments_remaining == 0:
            return output(
                "`node` command doesn't take any arguments",
                error=True
            )
        output(console.col('\nStarting Node.', 'green') + '\n[type: .exit to return] ')
        system('node')
        output(console.col('Closed Node.', 'red'))

    elif command == 'django':
        if not arguments_remaining == 0:
            return output(
                "`django` command doesn't take any arguments",
                error=True
            )
        output(console.col('\nStarting Django.', 'green') + '\n[type: exit() to return] ')
        system(f'{executable} run.py shell_plus')
        output(console.col('Closed Django.', 'red'))

    elif command == 'status': system('git status')

    elif command == 'clear': system('clear')

    elif command == 'code': system('code .')

    elif command == 'sh':
        _process = subprocess.run(arguments, capture_output=True, text=True)
        output(_process.stdout)

    elif command == 'exit': exit()

    else:
        bad_input = ' '.join(command_line)
        output(f"No command matching input\n > ./o {bad_input}", error=True)

    return awaitInput(False)


def run():
    if len(command_line) <= 0:
        return awaitInput()
    [run_tool(arg, index) for index, arg in enumerate(command_line)]


if __name__ == '__main__':
    run()
