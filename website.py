# Framework Imports
from Overlord.Bionic.Local import Index, Server
from Overlord.Bionic.Basics import py_args, root
# Local App Imports
from Apps.ui import App
from appIndex import app_index

wsgi = Server.app


# Site Index
@Index.add('/')
def __index__():
    return App


# App Distributor
@Index.add('/dist')
def __distribution__():
    if 'app' in Server.request.args and \
        Server.request.args['app'] in app_index:
            return app_index[ Server.request.args['app']]
    return Server.goto('/')


# Boot Conditions
if __name__ == "__main__":
    if '-t' in py_args:
        wsgi.run(debug=True)
    else:
        wsgi.run(debug=False)
