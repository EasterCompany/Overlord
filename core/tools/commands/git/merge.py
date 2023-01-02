from sys import path
from os import system, chdir

git_cmd = '''
    git checkout main && git pull origin main &&
    git merge dev -m '{message}' &&
    git push origin main && git checkout dev
'''.replace('\n', ' ')


def with_message(message, module_name):
    module = module_name
    if module == 'server':
        module = None

    print('\n', module_name, ":------------------\n")
    if module is not None:
        chdir(path[0] + '/' + module)

    system(git_cmd.format(message=message))
    return print(''), chdir(path[0])


def all(message):
    print('\nSubmodules :------------------\n')
    system('''
        git submodule foreach --recursive "{git_cmd} && echo '' || :"
    '''.format(git_cmd=git_cmd.format(message=message)).\
        replace('\n', ' '))

    print('\nParent :----------------------\n')
    system(git_cmd)
    return print('')


def error_message():
    return print("""
    `MERGE` tool requires two arguments beginning with `-`

        ./o merge -all -"merge message"
        ./o merge -server -"merge message"
        ./o merge -clients -"merge message"
        ./o merge -tools -"merge message"
    """)
