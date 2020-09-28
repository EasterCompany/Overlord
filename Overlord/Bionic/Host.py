from Overlord.Bionic.Basics import platform_version, root, py_args, syspath
from Overlord.Bionic.Local import Server, Index


@Index.add('/o')
def __test_end_point__():
    return Server.test()


@Index.add('/o/user/add')
def __user_add__():
    new_user = Index.urp(
        'fname', 
        'lname',
        'passw'
    )
    return Server.make_new_user(new_user)


@Index.add('/o/user/remove')
def __user_remove__():
    user = Index.urp('uid', 'ukey')
    if Server.log_user(user):
        Server.remove_user(user['uid'])
        return Server.goto('/')
    else:
        return 'Failed to authenticate and remove user.'


@Index.add('/o/user/fetch')
def __user_global__():
    return Server.fetch_user(Index.urp('uid')['uid'])


@Index.add('/o/update')
def __client_update__():
    request = Index.urp('file')['file']
    if request == 'vers.ctrl':
        return str(platform_version())
    elif request is not None:
        try: return open(root + '/Overlord/' + request, 'r').read()
        except Exception as err: return str(err)
    return ''


if '-t' in py_args and syspath.exists(root + '/Tools'):
    from Tools import Atlas


    @Index.add('/o/atlas')
    def __library__():
        return Atlas.Tool.render()

