# Standard library
from sys import path
from pytest import main as test, ExitCode


def all_tests():
    print("")
    test_status = test([path[0]])
    if test_status and not test_status == ExitCode.NO_TESTS_COLLECTED:
        return False
    return True
