import importlib.util
from Overlord.Atlas.Test import new_set
from ..Bionic.Basics import cwd, syspath, mkdir, StrColor


class SystemMonitor:

    def __init__(self):
        self.project_dir = cwd().replace('\\', '/')
        self.directory = self.project_dir + "/Overlord/Atlas/tests"
        self.project = {
            'name': self.project_dir.split('/')[-1],
            'path': self.project_dir,
            'libs': dict()
        }

    def library(self, lib):

        def parse_function(f):
            data = str(f). \
                replace('<', '').replace('>', ''). \
                replace("'", '').replace('"', ''). \
                replace('(', '').replace(')', ''). \
                split(' ')
            if data[0] != 'built-in' or data[0] != 'module' and data[2] != 'namespace':
                if data[1] == 'abc':
                    print("[ERROR] cannot test python standard library module with Atlas.")
                    exit()
                try:
                    return {
                        'name': data[1],
                        'path': data[3],
                        'root': f,
                        'test': data[3].replace(
                            add.project['path'] + '/Overlord/' + data[1].split('.')[1],
                            'Overlord/Atlas/tests/' + '/'.join(data[1].split('.')[0:-1])
                        )
                    }
                except Exception as import_error:
                    return {
                        'name': data[1], 
                        'path': 'sub-module', 
                        'root': f, 
                        'test': 'Overlord/Atlas/tests/General/all.py'
                    }

        class Library:

            def __init__(self, library, *args, **kwargs):
                self.library = {
                    'root': library,
                    'modules': {},
                }
                for name, value in library.__dict__.items():
                    if not name.startswith('__') and not name.endswith('__'):
                        mod = parse_function(value)
                        if not self.test_file_exists(mod):
                            self.make_test_file(mod)
                        self.library['modules'][name] = mod

            @staticmethod
            def test_file_exists(mod):
                return syspath.exists(mod['path'].replace(add.project_dir, add.directory))

            @staticmethod
            def make_test_file(mod):
                print('>> new test file :', mod['test'], '\n')
                mod_dir = add.project_dir + '/' + mod['test']
                mkdir('/'.join(mod_dir.split('/')[0:-1]))
                test_file = open(mod_dir, "w+")

                if '.' in mod['name']:
                    import_statement = [
                        "from", 
                        '.'.join(mod['name'].split('.')[0:-1]),
                        "import",
                        mod['name'].split('.')[-1],
                        "as sut"
                    ]
                else:
                    import_statement = [
                        "import", 
                        mod['name'], 
                        'as sut'
                    ]

                test_file.write(
                    ' '.join(import_statement) + """
from Overlord.Atlas.Test import *


def test():
    return None

"""
                )
                test_file.close()

            def data(self):
                return self.library

        self.project['libs'][lib.__name__] = Library(lib).data()
        return self.project['libs'][lib.__name__]


class TestSuite:

    def __init__(self):
        print(
            '\n', add.project['name'], 'Test Suite\n',
            StrColor().black(add.project['path']), '\n'
        )
        self.target = add.project

    def run_tests(self):
        for LIB in self.target['libs']:
            new_set()
            print(LIB)
            
            for MODULE in self.target['libs'][LIB]['modules']:
                mod = self.target['libs'][LIB]['modules'][MODULE]
                test_path = mod['test'].replace('Overlord/Atlas/tests/', '/')
                spec = importlib.util.spec_from_file_location(mod['name'], mod['test'])
                mock = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mock)
                
                try:
                    result = mock.test()
                    if result is None:
                        result = {
                            'failed': 0,
                            'passed': 0
                        }
                    elif isinstance(result, bool):
                        if result:
                            result = {
                                'failed': 0,
                                'passed': 1
                            }
                        else:
                            result = {
                                'failed': 1,
                                'passed': 0
                            }
                except Exception as mock_error:
                    if str(mock_error).endswith("has no attribute 'test'"):
                        result = {
                            'failed': 0,
                            'passed': 0
                        }

                if result['failed'] > 0:
                    print('   ', StrColor().red(MODULE), StrColor().black(test_path))
                    if result['passed'] > 0:
                        print('     ', StrColor().green('Passed ' + str(result['passed'])),
                              StrColor().red('Failed ' + str(result['failed'])))
                    else:
                        print('     ', StrColor().red('Failed ' + str(result['failed'])))
                elif result['passed'] > 0:
                    print('   ', StrColor().green(MODULE), StrColor().black(test_path))
                else:
                    print('   ', StrColor().white(MODULE), StrColor().black(test_path))
        print('\n\n')


add = SystemMonitor()
run = TestSuite().run_tests
