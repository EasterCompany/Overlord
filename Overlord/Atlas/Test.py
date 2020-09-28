from Overlord.Bionic.Basics import syspath

Passed = True 
Failed = False
Result = {
    'passed': 0,
    'failed': 0,
}


def new_set():
    global Result
    Result = {
        'passed': 0,
        'failed': 0,
    }


def Pass():
    global Result
    Result['passed'] = Result['passed'] + 1


def Fail():
    global Result
    Result['failed'] = Result['failed'] + 1


def isEqual(a, b):
    return a == b


def isNotEqual(a, b):
    return a != b


def isNone(sut):
    return sut is None


def isNotNone(sut):
    return sut is not None


def pathExists(path):
    return syspath.exists(path)


def pathNotExists(path):
    return not syspath.exists(path)

