from os import system


def switch(branch):
    print(
        '\nEntering {branch_name} Branch\n\nParent :----------------------\n'.\
            format(branch_name=branch.\
                replace('dev', 'Development').\
                replace('main', 'Production')
            )
    )
    print("Entering 'Overlord'")
    system(
        'git checkout {branch} && git pull origin {branch} || true'.format(
            branch=branch
        )
    )
    system('git branch --set-upstream-to=origin/{branch} {branch}'.format(
        branch=branch
    ))
    print('\n\nSubmodules :------------------\n')
    system(
        'git submodule foreach --recursive "git checkout {branch} && git pull origin {branch} && git branch --set-upstream-to=origin/{branch} {branch} && echo "" || true"'.\
        format(
            branch=branch
        )
    )
    print('')
