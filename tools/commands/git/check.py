from re import sub
# Standard library
import subprocess
# Overlord library
from web.settings import BASE_DIR


def version():
  result = subprocess.run(
    [f"{BASE_DIR}/tools/scripts/git/check_version.sh"],
    bufsize=1,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    universal_newlines=True
  )
  if result.stdout == "0\n":
    print("Up-to-date")
  elif result.stdout == "1\n":
    print("New Updates!")
  elif result.stdout == "2\n":
    print("*")
  elif result.stdout == "3\n":
    print("Diverged")
