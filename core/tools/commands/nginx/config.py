import shlex
from getpass import getuser
from sys import executable
from core.library import console, exists
from web.settings import BASE_DIR, SECRET_DATA, PROJECT_NAME

sites_enabled_dir = "/etc/nginx/sites-enabled"
sites_available_dir = "/etc/nginx/sites-available"
sites_enabled_file = f"{sites_enabled_dir}/{PROJECT_NAME}"
sites_available_file = f"{sites_available_dir}/{PROJECT_NAME}"
application_domain = SECRET_DATA['DOMAIN_URL'] if not SECRET_DATA['DOMAIN_URL'].startswith('www.') else\
  SECRET_DATA['DOMAIN_URL'].replace('www.', '', 1)
site_available_conf_no_ssl = lambda: shlex.quote('''
server {
  listen 80;
  return 301 https://$host$request_uri;
}

server {
  server_name .''' + application_domain + '''
  listen 443 ssl;

  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  location /static {
    autoindex on;
    alias ''' + BASE_DIR + '''/static;
  }
}
''')
systemd_service_template = lambda: shlex.quote(f'''[Unit]
Description={PROJECT_NAME}
After=default.target
[Service]
ExecStart={BASE_DIR}/{PROJECT_NAME}.run
[Install]
WantedBy=default.target''')
run_prd_template = lambda: shlex.quote(f'''#!/bin/bash
cd {BASE_DIR}
{executable} -m gunicorn web.wsgi:application 127.0.0.1:8000''')


def create_service() -> bool:
  '''
  Creates a systemd service for this server to use in production
  '''
  systemd_service_file = systemd_service_template()
  console.sudo(f"rm /etc/systemd/system/{PROJECT_NAME}.service")
  console.sudo(f"touch {PROJECT_NAME}.service", cwd="/etc/systemd/system")
  console.sudo(f"echo {systemd_service_file} | sudo -S tee {PROJECT_NAME}.service", cwd="/etc/systemd/system")
  if exists(f"/etc/systemd/system/{PROJECT_NAME}.service"):
    return True
  return False


def create_runner() -> bool:
  '''
  Creates a bash script to run the server in production mode
  '''
  runner_file = run_prd_template()
  console.sudo(f"rm {BASE_DIR}/{PROJECT_NAME}.run")
  console.sudo(f"touch {PROJECT_NAME}.run", cwd=BASE_DIR)
  console.sudo(f"echo {runner_file} | sudo -S tee {PROJECT_NAME}.run", cwd=BASE_DIR)
  console.sudo(f"chmod +x {PROJECT_NAME}.run", cwd=BASE_DIR)
  if exists(f"{BASE_DIR}/{PROJECT_NAME}.run"):
    return True
  return False


def overwrite_nginx_conf() -> None:
  '''
  Removes any existing nginx.conf file and replaces it with Overlord's default one
  '''
  if exists("/etc/nginx/sites-available"):
    console.sudo("rm -rf /etc/nginx/sites-available")
  if exists("/etc/nginx/sites-enabled"):
    console.sudo("rm -rf /etc/nginx/sites-enabled")
  console.sudo("rm /etc/nginx/nginx.conf")
  console.sudo(f"cp {BASE_DIR}/core/tools/commands/nginx/assets/nginx.conf /etc/nginx/")


def create_www_data_user() -> None:
  '''
  Creates the www-data user on this system
  '''
  current_user = getuser()
  console.sudo("adduser  --no-create-home  --system  --user-group --shell /bin/false   www-data")
  console.sudo(f"usermod -a -G {current_user} www-data")


def generate_site_files() -> bool:
  '''
  Generates the site config files at /etc/nginx/sites-available & /etc/nginx/sites-enabled/ for this project
  '''
  file_contents = site_available_conf_no_ssl()

  if not exists(sites_available_dir):
    console.sudo(f"mkdir sites-available", cwd="/etc/nginx")
  if not exists(sites_enabled_dir):
    console.sudo(f"mkdir sites-enabled", cwd="/etc/nginx")
  if exists(sites_available_file):
    console.sudo(f"rm {sites_available_file}")
  if exists(sites_enabled_file):
    console.sudo(f"rm {sites_enabled_file}")

  console.sudo(f"touch {PROJECT_NAME}", cwd=sites_available_dir)
  console.sudo(f"echo {file_contents} | sudo -S tee {PROJECT_NAME}", cwd=sites_available_dir)
  console.sudo(f"ln -sf {sites_available_file} {sites_enabled_dir}", cwd=sites_available_dir)

  if exists(sites_available_file) and exists(sites_enabled_file):
    return True
  return False


def generate_ssl_certificate() -> None:
  '''
  Generates the ssl certificates using certbot for nginx, this will also create a cronjob which automatically
  renews the certificates once per year before they expire
  '''
  if len(application_domain) == 0:
    console.status("warn", "You have not set a DOMAIN_URL configuration in your\n  .config/secrets.json file")
  console.input("sudo certbot --nginx", show_output=True)
  console.input("sudo certbot renew --dry-run")
