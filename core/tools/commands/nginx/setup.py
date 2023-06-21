# Automate Nginx Gateways for Overlord Web Apps
# Currently only available for Unix based systems
from . import service, config
from core.library import exists, console, package


def run() -> None:
  if not console.verify(
    warning='''Using the Nginx automation tool via Overlord-CLI will
    overwrite any existing Nginx configurations on this system.

    You can proceed to customize your Nginx setup after using this
    command, however the initial setup will require overwriting some
    critical files.

    Some packages will attempt to be installed:
    nginx, certbot & python3-certbot-nginx
  '''): return

  console.out("> Installing packages")
  if not (package.apt_installed or package.yum_installed):
    console.out(f"  {console.failure} No package manager (apt/yum) found.", "red")
    console.out(f"  you will need to manually generate ssl certificates.", "red")
  else:
    console.out(f"  {console.wait} nginx", end="\r")
    package.install("nginx")
    console.out(f"  {console.success} nginx", "success")
    console.out(f"  {console.wait} certbot", end="\r")
    package.install("certbot")
    console.out(f"  {console.success} certbot", "success")
    console.out(f"  {console.wait} python3-certbot-nginx", end="\r")
    package.install("python3-certbot-nginx")
    console.out(f"  {console.success} python3-certbot-nginx", "success")

  if not exists("/etc/nginx"):
    console.status('error', 'Cannot find Nginx on this system @ /etc/nginx')
    return

  if service.stop() == 0:
    console.out("\n> Generating nginx.conf file")
    console.out(f"  {console.success} Stopped nginx service", "green")
  else:
    console.out(f"  {console.failure} Failed to stop nginx service", "red")
    return

  config.overwrite_nginx_conf()
  console.out(f"  {console.success} Created configuration files", "green")

  if service.start() == 0:
    console.out(f"  {console.success} Started nginx service", "green")
  else:
    console.out(f"  {console.failure} Failed to start nginx service", "red")
    return

  console.out("\n> Generating site files")
  site_file_status = config.generate_site_files()

  if site_file_status:
    console.out(f"  {console.success} Created site files", "green")
  else:
    console.out(f"  {console.failure} Failed to generate configuration files", "red")
    return

  console.out("\n> Generating SSL certificate")
  ssl_status = config.generate_ssl_certificate()

  if ssl_status:
    console.out(f"  {console.success} Created self-signed certificates")
  else:
    console.out(f"  {console.failure} Failed to create certificates")
    return

  if service.restart() == 0:
    console.out(f"  {console.success} Restarted nginx service", "green")
  else:
    console.out(f"  {console.failure} Failed to restart nginx service", "red")
    return


def error_message() -> str:
  return console.out('''
  The `nginx` command requires at least one argument.

  nginx -setup
  nginx -start
  nginx -stop
  nginx -restart''')
