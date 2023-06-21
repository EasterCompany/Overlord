from core.library import console

stop = lambda: console.sudo("systemctl stop nginx", show_output=True)
start = lambda: console.sudo("systemctl start nginx", show_output=True)
restart = lambda: console.sudo("systemctl restart nginx", show_output=True)
reload = lambda: console.sudo("systemctl reload nginx", show_output=True)
