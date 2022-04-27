from sys import path
from os import system, chdir


def branch_origins(branch, repo=None):
    if repo is not None:
        chdir(path[0] + '/' + repo)
    system('git branch --set-upstream-to=origin/{branch} {branch}'.format(
        branch=branch
    ))
    return chdir(path[0])


def all():
    chdir(path[0])
    print('\nSubmodules :------------------\n')
    system('''git submodule foreach --recursive "git pull && echo ''"''')
    print('\nParent :----------------------\n')
    system('git pull')
    print('')
