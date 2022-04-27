# Standard library
import json
from os import chdir, getcwd
from importlib import util
from os.path import exists
from datetime import datetime

# Sort directory for tests
if getcwd().endswith('tasks/daily'):
    settings_directory = "../../web/settings.py"
else:
    settings_directory = "web/settings.py"

# Import projects settings
web_mod = util.spec_from_file_location("settings.py", settings_directory)
settings = util.module_from_spec(web_mod)
web_mod.loader.exec_module(settings)
log_path = settings.BASE_DIR + '/.logs/cpu_usage.json'

# Go to project directory
chdir(settings.BASE_DIR)

# Project API directory
api_mod = util.spec_from_file_location("api.py", "tools/commands/pa/api.py")
pa_api = util.module_from_spec(api_mod)
api_mod.loader.exec_module(pa_api)
fetch_api = pa_api.fetch_api


def load_log():
    if exists(log_path):
        with open(log_path) as log_file:
            log_data = json.loads(log_file.read())
        return log_data
    return {}


def save_log(new_data):
    with open(log_path, 'w+') as log_file:
        json.dump(new_data, log_file, indent=2)


def get_cpu_data():
    data = fetch_api('cpu')
    cpu_limit = int(data['daily_cpu_limit_seconds'])
    cpu_usage = round(
        float(data['daily_cpu_total_usage_seconds']), 2
    )
    cpu_perct = round(
        (100 / cpu_limit) * cpu_usage, 1
    )
    date = datetime.now().strftime("%Y/%m/%d")
    return cpu_limit, cpu_usage, cpu_perct, date


def log_cpu_data(data=None):
    log = load_log()
    if data is None:
        cpu_limit, cpu_usage, cpu_perct, date = get_cpu_data()
    else:
        cpu_limit, cpu_usage, cpu_perct, date = data
    log[date] = {
        'usage': cpu_usage,
        'limit': cpu_limit,
        'percent': cpu_perct,
    }
    save_log(log)
    return log


if __name__ == '__main__':
    log_cpu_data()
