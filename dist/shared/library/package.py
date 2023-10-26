from .console import console

yum_installed = bool(console.input("command -v yum"))
apt_installed = bool(console.input("command -v apt-get"))


def install(package:str) -> bool:
  if apt_installed:
    console.sudo(f"apt-get install -y {package}")
    return True
  elif yum_installed:
    console.sudo(f"yum install -y {package}")
    return True
  else:
    console.out("  [ERROR] No package manager (apt/yum) was found.", "red")
  return False


def update() -> bool:
  if apt_installed:
    console.sudo(f"apt-get update -y")
    return True
  elif yum_installed:
    console.sudo(f"yum update -y")
    return True
  return False
