# TODO: Deprecated file needs removed

# Standard library
import json
from sys import path
from os import system
from datetime import datetime
# Overlord library
from core.tools.commands.git import pull

# Load requests logs file for logging
with open(path[0] + '/.logs/requests.json') as requests_file:
    requests_logs = json.loads(requests_file.read())

# Load secrets for verification purposes
with open(path[0] + '/.config/secret.json') as secrets_file:
    secrets_data = json.loads(secrets_file.read())

# Universal status responses
OK_status = 'OK'
BAD_status = 'BAD'


def update_logs(new_log):
    global requests_file, requests_logs

    # Add timestamps to each log
    log_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
    log_iter = 0

    # If multiple requests received at the same time id each request
    while log_time in requests_logs:
        log_time += 'x' + str(log_iter)
        log_iter += 1

    # Append log to existing logs
    requests_logs[log_time] = new_log

    # Dump new logs to disk
    file_path = path[0] + '/.logs/requests.json'
    with open(file_path, 'w') as json_file:
        json.dump(
            requests_logs,
            json_file,
            indent=2
        )


def verify_request(req, secret):
    if secret == secrets_data['SERVER_KEY']:
        return True
    update_logs(
        {
            'req': req,
            'status': BAD_status,
            'verified': False
        }
    )
    return False


def upgrade_request(secret):
    req = 'upgrade'
    print('\nAn `UPGRADE REQUEST` was run.', '\nverifying request...')

    if not verify_request(req, secret):
        print('    failed.\n')
        return BAD_status

    print('    succeeded.\n')

    try:
        pull.all()                              # Pull updates from git repository
        system(path[0] + '/o collectstatic')    # Collect new static files
        status = OK_status
    except Exception as e:
        status = str(e)

    update_logs(                                # Log upgrade request
        {
            'req': req,
            'status': status,
            'verified': True
        }
    )

    return status
