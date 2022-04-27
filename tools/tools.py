# Standard library
from sys import argv, path

# Overlord library
from core.library.console import Console
from .library import console
from .commands import install, git, django, node, pytest, pa

tools_path = '/'.join(__file__.split('/')[:-1])
project_path = path[0]
command_line = argv[2:]
len_cmd_line = len(command_line)


def help():
    return print(
        ''' To get help & information on
 Overlord tools go to this github
 address

 https://github.com/EasterCompany/Overlord-Tools/blob/main/README.md

 or read your local README.md
 ------------------------------
    ''')


def run_tool(command, index=0):
    # General input variables
    arguments_remaining = 0
    arguments = []
    con = Console()

    for arg in command_line[index + 1:]:
        if arg.startswith('-'):
            arguments_remaining += 1
            arguments.append('-'.join(arg.split('-')[1:]))
        else:
            break

    # Used for commit & merge commands
    if arguments_remaining >= 2:
        git_repo = ''.join(
            command_line[index + 1].split('-')[1:]
        )
        git_message = ''.join(
            ' '.join(command_line[index + 2:]).split('-')[1:]
        )
    else:
        git_repo, git_message = None, None

    if command.startswith('-'): return None

    elif command == 'install':
        if arguments_remaining > 0 and \
        (arguments[0] == 'clients' or arguments[0] == 'client'):
            if arguments_remaining == 1:
                return node.clients.install()
            elif arguments_remaining > 1:
                for argument in arguments[1:]:
                    node.clients.install(argument)
                return

        print('\nInstalling Overlord-Tools...')
        git.update.all()

        def set_branch_origins(repo=None):
            git.update.branch_origins('dev', repo)
            git.update.branch_origins('main', repo)

        set_branch_origins()
        set_branch_origins('clients')
        set_branch_origins('tools')
        print(' ')
        install.make_server_config(project_path)
        install.django_files(project_path)
        install.secrets_file(project_path)
        print('\n', console.col('Done.', 'green'), '\n')

    elif command == 'update':
        git.update.all()

    elif command == 'dev' or command == 'development':
        git.branch.switch('dev')

    elif command == 'main' or command == 'production':
        git.branch.switch('main')

    elif command == 'merge':
        if arguments_remaining == 2:
            if arguments[0] == 'all': git.merge.all(git_message), exit()
            else: git.merge.with_message(git_message, git_repo), exit()
        git.merge.error_message(), exit()

    elif command == 'push':
        git.push.all()

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
            exit(99)

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
        if arguments_remaining == 1:
            return node.clients.create(arguments[0])
        else:
            return node.clients.error_message()

    elif command == 'share':
        if arguments_remaining == 2:
            return node.share.target(arguments[0], arguments[1])
        else:
            return node.share.error_message()

    elif command == 'help': help()

    else: print('invalid input \n  >> ./o', ' '.join(command_line))

    return exit()


def run():
    if len(argv) <= 2: help()
    else: [run_tool(arg, index) for index, arg in enumerate(command_line)]


if __name__ == '__main__':
    run()
