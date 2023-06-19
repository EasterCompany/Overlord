# Automate Nginx Gateways for Overlord Server
# Currently only available for Unix based systems
import shlex
from core.library import exists, console, sudo
from web.settings import PROJECT_NAME, BASE_DIR

site_available_conf = lambda: shlex.quote('''
# HTTP Redirect to HTTPS
server {
  listen 80;
  return 301 https://$host$request_uri;
}

# HTTPS /w SSL Certificate
server {
  listen 443 ssl;
  #ssl_certificate /etc/letsencrypt/live/findseo.net/fullchain.pem;
  #ssl_certificate_key /etc/letsencrypt/live/findseo.net/privkey.pem;
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


@sudo
def generate_config_files(sudo_pass:str, *args, **kwargs) -> str|int:
  '''
    Generates config files at /etc/nginx/sites-available & /etc/nginx/sites-enabled/
    for this project.
  '''
  site_enabled_conf_path = f'/etc/nginx/sites-enabled/{PROJECT_NAME}'
  site_available_conf_path = f'/etc/nginx/sites-available/{PROJECT_NAME}'
  file_contents = site_available_conf()

  if exists(site_available_conf_path):
    console.input(f'''echo {sudo_pass} | sudo -S rm {site_available_conf_path}''')
  console.input(
    f'''echo {sudo_pass} | sudo -S touch {PROJECT_NAME} && echo {file_contents} | sudo -S tee {PROJECT_NAME}''',
    cwd="/etc/nginx/sites-available",
    show_output=True
  )

  console.input(
    f'''echo {sudo_pass} | sudo ln -sf {site_available_conf_path} /etc/nginx/sites-enabled/''',
    show_output=True
  )

  if exists(site_available_conf_path) and exists(site_enabled_conf_path):
    return True
  return False


@sudo
def restart(sudo_pass:str, *args, **kwargs) -> str|int:
  ''' Restarts the nginx service on this machine '''
  return console.input(
    f'''echo {sudo_pass} | sudo -S systemctl restart nginx'''
  )


@sudo
def run(sudo_pass:str = "", *args, **kwargs) -> str|int:
  ''' Runs the initial setup process for nginx on this machine '''
  conf_generation = generate_config_files(sudo_pass)

  console.out('\n> Generating Nginx Config Files')
  if not conf_generation:
    return console.out(
      f'  {console.failure} Failed to generate configuration files,\n    does the current user have root permissions?',
      'red'
    )
  console.out(f'  {console.success} Configuration files exist', 'green')
  restart(sudo_pass)
  return console.out(f'  {console.success} Restarted nginx service', 'green')


def error_message() -> str:
  return console.out('''
  The `nginx` command requires at least one argument.

  nginx -setup

  or

  nginx -restart''')
