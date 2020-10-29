from .Basics import platform_version, root
from .Local import Server, Index


@Index.add('/test')
def test():
    return Server.test()


@Index.add('/user/add')
def user_add():
    new_user = Server.parse_user(
        Index.urp('email', 'passw')
    )
    return Server.make_new_user(new_user)


@Index.add('/user/remove')
def user_remove():
    user = Index.urp('email', 'passw')
    if Server.log_user(user):
        Server.remove_user(user['email'])
        return Server.goto('/')
    else:
        return 'Failed to authenticate and remove user.'


@Index.add('/user/auth')
def user_auth():
    user = Server.parse_user(
        Index.urp('email', 'passw')
    )
    token = Server.log_user(user)
    if token is not None:
        return token
    else:
        return str()


@Index.add('/user/end')
def user_end():
    print(Index.urp('token')['token'])
    response = Server.end_user(
        Index.urp('token')['token']
    )
    print(response)
    return 'logged out'


@Index.add('/update')
def client_update():
    request = Index.urp('file')['file']
    if request == 'vers.ctrl':
        return str(platform_version())
    elif request is not None:
        try: return open(root + '/Overlord/' + request, 'r').read()
        except Exception as err: return str(err)
    return ''

