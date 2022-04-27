# Standard library
from os import remove

# Overlord library
from tasks.daily import track_cpu_usage as sut


def test_logging():
    delete_log_after_save = False
    log = {}
    len_log = len(log)

    # Test initial load behaves as expected
    if sut.exists(sut.log_path):
        log = sut.load_log()
        if 'test' in log:
            assert len(log) == 1
            del log['test']
        else:
            assert len(log) != 0
        len_log = len(log)
    else:
        log = sut.load_log()
        assert len(log) == 0
        delete_log_after_save = True

    # Test initial save behaves as expected
    assert 'test' not in log
    log['test'] = {'input': 'test'}
    sut.save_log(log)
    assert sut.exists(sut.log_path)

    log = sut.load_log()
    assert log['test']['input'] == 'test'
    assert len(log) == len_log + 1 and len(log) != 0

    cpu_limit, cpu_usage, cpu_perct, date = sut.get_cpu_data()
    assert isinstance(cpu_limit, int)
    assert isinstance(cpu_usage, float)
    assert isinstance(cpu_perct, float)
    assert isinstance(date, str)

    new_log = sut.log_cpu_data(
        [cpu_limit, cpu_usage, cpu_perct, date + ' test']
    )

    assert date + ' test' in new_log
    assert new_log[date + ' test']['usage'] == cpu_usage
    assert new_log[date + ' test']['limit'] == cpu_limit
    assert new_log[date + ' test']['percent'] == cpu_perct

    # If the log file did not exist before; delete it
    if delete_log_after_save:
        remove(sut.log_path)
        assert not sut.exists(sut.log_path)
    else:
        log = sut.load_log()
        del log['test']
        del log[date + ' test']
        sut.save_log(log)
        log = sut.load_log()
        assert 'test' not in log
        assert date + ' test' not in log
        if len(log) == 0:
            remove(sut.log_path)
            assert not sut.exists(sut.log_path)
