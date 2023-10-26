# Overlord library
from .api import domain, server
from core.library import console


def request():
  print(f'\n> Upgrade Server @ {domain}')
  console.out(f"  {console.wait} Upgrading ...", end="\r")

  data = server('upgrade')
  console.out(
    "  ✅ Server Upgraded  ", "success"
  ) if data['status'] == "OK" else console.out(
    "  ⚠️ Unknown Error ",
  )

  return data
