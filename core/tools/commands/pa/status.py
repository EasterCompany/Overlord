# Standard library
import re
import requests
from time import time
from requests_html import HTMLSession
# Overlord library
from .api import domain, server
from core.library import console


def request():
  start_time = time()
  console.out(f'\n> Status Check @ {domain}')
  console.out(f'  {console.wait} Testing API ...', end="\r")
  data = server('status')

  if 'error' not in data:
    console.out(
      "  ✅ Server API Responded  ", "success"
    ) if data['status'] == "OK" else console.out(
      "  ⚠️ Unknown Error         "
    )
    response = requests.get(f'https://{domain}/')
  elif 'error' in data:
    console.out(
      f"  🔥 Sever API Not Responding  ", "error"
    )

  console.out(f'  {console.wait} Testing Client ...', end="\r")
  client_is_served = re.search(
    """<script defer="defer" src="/static/.*/static/js/main..*.js"></script>"""
    """<link href="/static/.*/static/css/main..*.css" rel="stylesheet">""",
    response.content.decode('utf-8')
  )

  # App Served Status
  if client_is_served:
    console.out("  ✅ Client Served         ", "success")
  else:
    console.out("  🔥 Client Not Served     ", "error")
    console.out("  🔥 Client Not Rendered   ", "error")

  # App Renders Status
  if client_is_served:
    console.out(f"  {console.wait} Rendering Client ...", end="\r")

    try:
      session = HTMLSession()
    except:
      return console.out("  ⚠️ Failed To Test Client  ")

    try:
      client = session.get(f"https://{domain}/")
      client.raise_for_status()
    except:
      return console.out("  🔥 Failed To Access Domain")

    try:
      client.html.render()
    except:
      return console.out("  🔥 Failed To Render Client")

    end_time = time()
    console.out("  ✅ Client Rendered         ", "success")
    console.out(f"\n  Tests Completed Successfully ({round(end_time-start_time, 4)}s)", "success")

  return data
