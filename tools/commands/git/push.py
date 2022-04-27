from os import system


def all():
    print('\nSubmodules :------------------\n')
    system('''git submodule foreach --recursive "git push && echo ''"''')
    print('\nParent :----------------------\n')
    system('git push')
    print('')
