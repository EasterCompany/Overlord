# Framework Imports
from Overlord.Bionic.Local import Index, Server
from Overlord.Bionic.Basics import py_args, root
# Local App Imports
from Apps.ui import App
from appIndex import app_index


# Site Index
@Index.add('/')
def __index__():
    return App


# App Distributor
@Index.add('/dist')
def __distribution__():
    if 'app' in Server.request.args:
        dist_app = Server.request.args['app']
    else:
        return Server.goto('/')
    if dist_app in app_index:
        return app_index[dist_app]
    return str()


# Boot Conditions
if __name__ == "__main__":
    if '-t' in py_args:
        Server.app.run(debug=True)
    else:
        Server.app.run(debug=False)
