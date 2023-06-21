import shlex
from core.library import console, exists, mkdir
from web.settings import BASE_DIR, SECRET_DATA, PROJECT_NAME

sites_enabled_dir = "/etc/nginx/sites-enabled"
sites_available_dir = "/etc/nginx/sites-available"
sites_enabled_file = f"{sites_enabled_dir}/{PROJECT_NAME}"
sites_available_file = f"{sites_available_dir}/{PROJECT_NAME}"
application_domain = SECRET_DATA['DOMAIN_URL']
site_available_conf = lambda: shlex.quote('''
server {
  listen 80;
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl;
  #ssl_certificate /etc/letsencrypt/live/''' + application_domain + '''/fullchain.pem;
  #ssl_certificate_key /etc/letsencrypt/live/''' + application_domain + '''/privkey.pem;
  #include /etc/letsencrypt/options-ssl-nginx.conf;
  #ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

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


def generate_site_files() -> bool:
  '''
  Generates the site config files at /etc/nginx/sites-available & /etc/nginx/sites-enabled/ for this project
  '''
  file_contents = site_available_conf()

  if not exists(sites_available_dir):
    console.sudo(f"mkdir {sites_available_dir}")
  if not exists(sites_enabled_dir):
    console.sudo(f"mkdir {sites_enabled_dir}")
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


def generate_ssl_certificate() -> bool:
  '''

  '''
  return True
