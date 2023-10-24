from core.library import console, package


def run() -> None:
  console.out("\n> Download & Install Redis")
  package.update()
  install_dependencies()
  package.update()
  console.out(f"  {console.wait} redis", end="\r")
  package.install("redis")
  console.out(f"  {console.success} redis", "success")


def install_dependencies() -> None:
  console.out("> Installing Dependencies")

  console.out(f"  {console.wait} lsb-release", end="\r")
  package.install("lsb-release")
  console.out(f"  {console.success} lsb-release", "success")

  console.out(f"  {console.wait} curl", end="\r")
  package.install("curl")
  console.out(f"  {console.success} curl", "success")

  console.out(f"  {console.wait} gpg", end="\r")
  package.install("gpg")
  console.sudo(
    """curl -fsSL https://packages.redis.io/gpg | """
    """sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg"""
  )
  console.sudo(
    """echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] """
    """https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list"""
  )
  console.out(f"  {console.success} gpg", "success")


def error_message() -> str:
  return console.out('''
  The `redis` command requires at least one argument.

  redis -setup
  redis -test''')
