# Local app imports
from .api import fetch_api


def display():
  a_tasks = fetch_api('always_on')
  print('\n', ':------------------ TASKS INFO ------------------:\n')

  for task in a_tasks:
    print(task + ':\n    ', a_tasks[task])

  s_tasks = fetch_api('schedule')
  for task in s_tasks:
    print(' ', task['id'], task['interval'], task['printable_time'],
      '\n ', task['command'].split('/')[-1],
      '\n ', 'http://eu.pythonanywhere.com' + task['logfile'],
      '\n'
    )
  print(' :------------------------------------------------:\n')
