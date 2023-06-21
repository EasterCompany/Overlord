import shlex
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
site_available_conf = lambda: shlex.quote('''
server {
  listen 80;
  return 301 https://$host$request_uri;
}

server {
  server_name .''' + application_domain + '''
  listen 443 ssl;
  ssl_certificate /etc/letsencrypt/live/''' + application_domain + '''/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/''' + application_domain + '''/privkey.pem;
  include /etc/letsencrypt/options-ssl-nginx.conf;
  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

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


def create_www_data_user() -> str|int:
  '''
  Creates the www-data user on this system
  '''
  return console.sudo("adduser  --no-create-home  --system  --user-group --shell /bin/false   www-data")


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
  console.input(
    "sudo -S certbot --nginx"
    " --register-unsafely-without-email --renew-by-default"
    f" -d {application_domain} -d *.{application_domain}"
    ' --pre-hook "sudo systemctl stop nginx" --post-hook "sudo systemctl start nginx"',
    show_output=True
  )
  console.sudo("certbot renew --dry-run")
