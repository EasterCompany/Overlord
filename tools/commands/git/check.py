from re import sub
# Standard library
import subprocess
# Overlord library
from tools.library.console import col
from web.settings import BASE_DIR


def check_version_status():
  result = subprocess.run(
    [f"{BASE_DIR}/tools/scripts/git/check_version.sh"],
    bufsize=1,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    universal_newlines=True
  )
  if result.stdout == "0\n": return ["", "white"]
  elif result.stdout == "1\n": return ["[New Update Available]\n", "green"]
  elif result.stdout == "2\n": return ["   [Commits Pending]   \n", "yellow"]
  elif result.stdout == "3\n": return ["      [Diverged]       \n", "red"]


def version_status_label():
  _ver_str, _ver_col = check_version_status()
  return col(_ver_str, _ver_col)
