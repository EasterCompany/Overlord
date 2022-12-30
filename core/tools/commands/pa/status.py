# Standard library
import requests
# Overlord library
from .api import domain, server
from core.library import console


def request():
  print(f'\nChecking {domain} ...\n')
  data = server('status')

  if 'error' in data:
    msg = "SERVER IS DOWN!"
  else:
    msg = "Server API Responded" if data['status'] == "OK" else None
    console.out(f" ✅ {msg}", "success")
    response = requests.get(f'https://{domain}/')

  if 'error' in data:
    console.status(f" 🔥 {msg}", "error")
  elif 'data' in data and data['data'] == "[500] Internal server error.":
    print('REASON:', console.out(data['data'], 'red'))

  if b'{#prerender_status_check#}' in response.content:
    console.status(" ✅ Application Served", "success")
  else:
    console.out(f" 🔥 Application Failed", "error")

  return data
