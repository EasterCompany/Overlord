# Automate Nginx Gateways for Overlord Web Apps
# Currently only available for Unix based systems
from . import service, config
from core.library import exists, console, package


def run() -> None:
  if not console.verify(
    warning='''Using the Nginx automation tool via Overlord-CLI will
    overwrite any existing Nginx configurations on this system.

    To generate SSL certificates, certbot will be used so that your
    certificates will never expire and be renewed once per year
    automatically.

    Some packages will be installed:
    nginx, certbot & python3-certbot-nginx
  '''): return

  service.stop(show=False)
  console.out("> Installing packages")
  if not (package.apt_installed or package.yum_installed):
    console.out(f"  {console.failure} No package manager (apt/yum) found.", "error")
    return
  else:
    console.out(f"  {console.wait} nginx", end="\r")
    package.install("nginx")
    console.out(f"  {console.success} nginx", "success")
    console.out(f"  {console.wait} certbot", end="\r")
    if package.apt_installed:
      package.install("libaugeas0")
    elif package.yum_installed:
      package.install("augeas-libs")
    package.install("python3-venv")
    console.sudo("python3 -m venv /opt/certbot/")
    console.sudo("/opt/certbot/bin/pip install --upgrade pip")
    console.sudo("/opt/certbot/bin/pip install certbot")
    console.sudo("/opt/certbot/bin/pip install certbot-nginx")
    console.sudo("rm -rf /usr/bin/certbot")
    console.sudo("ln -s /opt/certbot/bin/certbot /usr/bin/certbot")
    console.out(f"  {console.success} certbot", "success")

  if not exists("/etc/nginx"):
    console.status("error", "Cannot find Nginx on this system @ /etc/nginx")
    return

  console.out("\n> Creating www-data user")
  config.create_www_data_user()
  console.out(f"  {console.success} Created user", "success")

  if service.stop() == 0:
    console.out("\n> Generating nginx.conf file")
    console.out(f"  {console.success} Stopped nginx service", "success")
  else:
    console.out(f"  {console.failure} Failed to stop nginx service", "error")
    return

  config.overwrite_nginx_conf()
  console.out(f"  {console.success} Created configuration files", "success")

  if service.start() == 0:
    console.out(f"  {console.success} Started nginx service", "success")
  else:
    console.out(f"  {console.failure} Failed to start nginx service", "error")
    return

  console.out("\n> Generating site files")
  site_file_status = config.generate_site_files()

  if site_file_status:
    console.out(f"  {console.success} Created site files", "success")
  else:
    console.out(f"  {console.failure} Failed to generate configuration files", "error")
    return

  console.out("\n> Starting nginx service")
  if service.start() == 0:
    console.out(f"  {console.success} Successfully configured SSL", "success")
    console.out(f"  {console.success} Started nginx service", "success")
  else:
    console.out(f"  {console.failure} Failed to restart nginx service", "error")
    return

  console.out("\n> Generating SSL certificate")
  if config.generate_ssl_certificate():
    if service.stop() == 0:
      console.out(f"  {console.success} Stopped nginx service", "success")
    else:
      console.out(f"  {console.failure} Failed to stop nginx service", "error")
      return
    console.out(f"  {console.success} Created SSL certificates")
  else:
    console.out(f"  {console.failure} Failed to create certificates")
    return


def error_message() -> str:
  return console.out('''
  The `nginx` command requires at least one argument.

  nginx -setup
  nginx -start
  nginx -stop
  nginx -restart''')
