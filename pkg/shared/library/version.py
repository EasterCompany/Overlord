import platform


class Version():
  overlord = {
    "major": 1,
    "minor": 3,
    "patch": 0
  }
  system = {
    "os": platform.system(),
    "git": "",
    "nginx": "",
    "go": "",
    "python": "",
    "node": ""
  }

  def __str__(self):
    return f"{self.overlord['major']}.{self.overlord['minor']}.{self.overlord['patch']} ({self.system['os']})"


__version__ = Version()
