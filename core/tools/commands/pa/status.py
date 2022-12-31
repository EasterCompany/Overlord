# Standard library
import re
import requests
# Overlord library
from .api import domain, server
from core.library import console


def request():
  console.out(f'\n> Status Check @ {domain}')
  console.out(f'  {console.wait} Testing API ...', end="\r")
  data = server('status')

  if 'error' not in data:
    console.out(
      "  ✅ Server API Responded  ", "success"
    ) if data['status'] == "OK" else console.out(
      "  ⚠️ Received Unexpected Response  "
    )
    response = requests.get(f'https://{domain}/')
  elif 'error' in data:
    console.out(
      f"  🔥 Sever API Not Responding  ", "error"
    )

  console.out(f'  {console.wait} Testing Client ...', end="\r")
  app_is_served = re.search(
    """<script defer="defer" src="/static/.*/static/js/main..*.js"></script>"""
    """<link href="/static/.*/static/css/main..*.css" rel="stylesheet">""",
    response.content.decode('utf-8')
  )

  if app_is_served:
    console.out("  ✅ Client Served         ", "success")
  else:
    console.out("  🔥 Client Not Served     ", "error")

  return data
