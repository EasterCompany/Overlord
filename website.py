from Overlord.Bionic.Local import Index, Server
from Overlord.Bionic.Basics import py_args
from Apps import Home


@Index.add('/')
def __home__():
    return Home.App.render()


if __name__ == "__main__":
    if '-t' in py_args:
        Server.app.run(debug=True)
    else:
        Server.app.run(debug=False)

