# Displays the system status when the CLI opens.
# To add more details, insert them into the 'status' dictionary.
import platform
from os import system
from os.path import exists
from sys import executable
from subprocess import getoutput
from web.settings import BASE_DIR
from core.tools import __version__ as ver

is_windows = platform.system() == "Windows"
window_width = 128 if is_windows else int(getoutput("tput cols"))
draw_width = 65
margin = " " * int((window_width - draw_width) / 2)
divider = "-" * int(draw_width)
status = {
  "storage": getoutput(
    """
    __disk_usage__=$(df -BG / | tail -n 1)
    __disk_total__=$(echo $__disk_usage__ | awk '{print $2}' | sed 's/G//')
    __disk_used__=$(echo $__disk_usage__ | awk '{print $3}' | sed 's/G//')
    echo "$__disk_used__/$__disk_total__ (GB)"
    """
  ),
  "memory": getoutput(
    """
    __mem_total__=$(grep MemTotal /proc/meminfo | awk '{printf "%.0f", $2/1024}')
    __mem_used__=$(free -m | awk 'NR==2{printf "%.0f", $3}')
    echo "$__mem_used__/$__mem_total__ (MB)"
    """
  ),
  "python": getoutput(executable + " -V 2>&1 | awk '{print $2}'"),
  "nginx": getoutput("nginx -v 2>&1 | awk -F '/' '{print $2}'"),
  "node": getoutput("node -v | sed 's/v//'"),
  "npm": getoutput("npm -v"),
  "git": getoutput("git --version | awk '{print $3}'")
}
colors = {
  "red": '\33[31m',
  "green": '\33[32m',
  "orange": '\33[33m',
  "blue": '\33[34m',
  "white": '\33[0m',
  "flash": '\33[5;30m',
}


def ascii_banner(color:str = 'orange') -> str:
  file_path = f"{BASE_DIR}/.banner"
  if exists(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
      raw = f.read()
      if '\n' in raw:
        lines = raw.split('\n')
        banner_draw_width = len(max(lines))
        banner_margin_width = int((window_width - banner_draw_width) / 2)
        banner_margin = " " * banner_margin_width
        banner = "\n".join([banner_margin + line + banner_margin for line in lines])
      else:
        banner = margin + raw + margin
      return f"{colors[color]}\n" + banner + colors['white']
  return ""


def status_table() -> str:
  table = f"{margin}{divider}{margin}\n"
  for key in status:
    value = status[key] if status[key] != 'bin' else ''
    table += f"{margin}{label(key,value)}{margin}\n"
  table += f"{margin}{divider}{margin}\n"
  return table


def label(key:str = "", value:str = "") -> str:
  left_pad = " " * int((draw_width / 2) - len(key) - 2)
  right_pad = " " * int((draw_width / 2) - len(value) - 2)
  return f"|{left_pad}{key.upper()}: {value}{right_pad}|"


def version() -> str:
  version_string = f"v{ver.major}.{ver.minor}.{ver.patch}"
  left_pad = " " * int((window_width - len(version_string)) / 2)
  right_pad = " " * int((window_width - len(version_string)) / 2)
  return f"{left_pad}{version_string}{right_pad}"


def display(show_status_table:bool = True, show_ascii_banner:bool = True, ascii_banner_color:str = 'orange'):
  system('cls') if is_windows else system('clear')
  if show_ascii_banner:
    print(ascii_banner(color=ascii_banner_color))
    print(version())
    print("")
  if show_status_table and not is_windows:
    print(status_table())
