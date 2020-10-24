from .Basics import platform_version, root, py_args, syspath
from .Local import Server, Index


@Index.add('/test')
def test():
    return Server.test()


@Index.add('/user/add')
def user_add():
    new_user = Index.urp(
        'email',
        'passw'
    )
    return Server.make_new_user(new_user)


@Index.add('/user/remove')
def user_remove():
    user = Index.urp('uid', 'ukey')
    if Server.log_user(user):
        Server.remove_user(user['uid'])
        return Server.goto('/')
    else:
        return 'Failed to authenticate and remove user.'


@Index.add('/user/fetch')
def user_global():
    return Server.fetch_user(Index.urp('uid')['uid'])


@Index.add('/update')
def client_update():
    request = Index.urp('file')['file']
    if request == 'vers.ctrl':
        return str(platform_version())
    elif request is not None:
        try: return open(root + '/Overlord/' + request, 'r').read()
        except Exception as err: return str(err)
    return ''

