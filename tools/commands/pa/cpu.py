# Standard library
from datetime import datetime
# Local app imports
from .api import fetch_api
from tools.library import console


def display():
    data = fetch_api('cpu')
    print('\n', ':------ CPU QUOTA INFO ------:\n')

    cpu_limit = int(data['daily_cpu_limit_seconds'])
    cpu_usage = round(
        float(data['daily_cpu_total_usage_seconds']), 2
    )
    cpu_perct = round(
        (100 / cpu_limit) * cpu_usage, 1
    )

    cpu_status = 'green'
    if cpu_perct >= 80:
        cpu_status = 'red'
    elif cpu_perct >= 50:
        cpu_status = 'yellow'

    print(
        '  Daily usage\n',
        '   ', str(cpu_usage) + 's', '/', str(cpu_limit) + 's',
        '   ', console.col(str(cpu_perct) + '%\n', cpu_status)
    )

    cpu_reset_datetime = datetime.strptime(
        data['next_reset_time'],
        '%Y-%m-%dT%H:%M:%S.%f'
    )
    cur_datetime = datetime.now()
    cpu_reset_at = str(cpu_reset_datetime - cur_datetime)
    cpu_reset_in = datetime.strptime(cpu_reset_at, '%H:%M:%S.%f').\
        strftime('%H:%M:%S')

    print(
        '  Time to reset\n',
        '   ', cpu_reset_in, '     ',
        cpu_reset_datetime.strftime('%H:%M:%S'),'\n'
    )
    print(' :----------------------------:\n')
