from Overlord.Bionic.Basics import open_file


def svg(name, folder='./Static/SVG'):
    return open_file(folder, name + ".svg").replace('\n', ' ')

