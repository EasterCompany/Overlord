from platform import uname
from sys import executable as py_exe, argv as py_args
from sqlite3 import connect as make_db
from os import getcwd as cwd, path as syspath, mkdir as __mkdir__,\
    system as system_terminal, execl, scandir
from subprocess import run as terminal
from random import *

root = cwd()


def log(*args):
    for arg in args:
        if callable(arg): 
            print(arg())
        else: 
            print(arg)


def mkdir(path):
    current_path = ''
    for part in path.replace('\\', '/').split('/'):
        '''
        . represents root on Unix systems
        : represents drive letter on Windows systems
        '''
        if not part == '.' and not part.endswith(':'):
            current_path += '/' + part
            if not syspath.exists(current_path):
                __mkdir__(current_path)
        else:
            current_path += part


def open_file(path, filename, forceful=False):
    if forceful:
        if not syspath.exists(path):
            mkdir(path)
        if not syspath.exists(path + '/' + filename):
            return open(path + '/' + filename, 'w+').read()
    return open(path + '/' + filename, 'r').read()


def local_db():
    mkdir(root + '/Overlord/.local')
    return make_db(root + "/Overlord/.local/local.db")


class StrColor:
    content = None
    close_string = '\033[0m'

    def __init__(self, as_string_with_colour=""):
        self.content = str(as_string_with_colour)

    def white(self, string=""):
        return '\033[97m' + str(string) + self.close_string

    def cyan(self, string=""):
        return '\033[96m' + str(string) + self.close_string

    def purple(self, string=""):
        return '\033[95m' + str(string) + self.close_string

    def blue(self, string=""):
        return '\033[94m' + str(string) + self.close_string

    def yellow(self, string=""):
        return '\033[93m' + str(string) + self.close_string

    def green(self, string=""):
        return '\033[92m' + str(string) + self.close_string

    def red(self, string=""):
        return '\033[91m' + str(string) + self.close_string

    def black(self, string=""):
        return '\033[90m' + str(string) + self.close_string

    def scored(self, string=""):
        return '\033[9m' + str(string) + self.close_string

    def invisible(self, string=""):
        return '\033[8m' + str(string) + self.close_string

    def highlight(self, string=""):
        return '\033[7m' + str(string) + self.close_string

    def blink(self, string=""):
        return '\033[6m' + str(string) + self.close_string

    def flash(self, string=""):
        return '\033[5m' + str(string) + self.close_string

    def underline(self, string=""):
        return '\033[4m' + str(string) + self.close_string

    def italic(self, string=""):
        return '\033[3m' + str(string) + self.close_string

    def bold(self, string=""):
        return '\033[1m' + str(string) + self.close_string


def run_python(command):
    return terminal(py_exe + " " + command, capture_output=True).stdout


def clear_console():
    if uname().system == 'Linux':
        return system_terminal('clear')


def reboot():
    if '-t' in py_args:
        return exit()
    return execl(py_exe, '"{}"'.format(py_exe), *py_args)


def version_control(target='version'):
    verst = open_file(root + '/Overlord/', 'vers.ctrl', True)
    if '\n' not in verst: 
        return str(0.0)
    else:
        verst = str(verst).split('\n')
        for arg in verst:
            if '=' not in arg or arg.startswith('#'):
                pass
            else:
                r = arg.split('=')
                if r[0] == target:
                    return r[1]
        return None


def platform_version():
    return float(version_control(target='version'))


def directory(r=dict(), d=root + '/', src=dict()):
    source = {
        'code': 0, 'cache': 0, 'chars': 0,
        'git': 0, 'db-file': 0, 'lines': 0,
        'ctrl-file': 0, 'untracked': 0,
    }
    files = dict()
    folders = dict()
    for f in scandir(d):
        if f.is_file():
            if f.name.endswith('.py') or f.name.endswith('.js'): source['code'] += 1
            elif f.name.endswith('.pyc') or f.name.startswith('.'): source['cache'] += 1
            elif '/.git' in d: source['git'] += 1
            elif f.name.endswith('.db'): source['db-file'] += 1
            elif f.name.endswith('.ctrl'): source['ctrl-file'] += 1
            else: source['untracked'] += 1
            try:
                files[f.name] = {
                    'name': f.name,
                    'content': open_file(d, f.name)
                }
                source['chars'] += len(files[f.name]['content'])
                source['lines'] += len(files[f.name]['content']\
                    .replace(';','\n').split('\n'))
            except Exception as file_error:
                files[f.name] = {
                    'name': f.name,
                    'content': str(file_error)
                }
        else:
            folders[f.name] = directory(d=d+f.name+'/')
            for s in folders[f.name]['source']:
                source[s] += folders[f.name]['source'][s]
    return {
        'path': d,
        'files': files,
        'folders': folders,
        'source': source
    }


project = directory()
