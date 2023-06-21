from core.library import console

stop = lambda show=True: console.sudo("systemctl stop nginx", show_output=show)
start = lambda show=True: console.sudo("systemctl start nginx", show_output=show)
restart = lambda show=True: console.sudo("systemctl restart nginx", show_output=show)
reload = lambda show=True: console.sudo("systemctl reload nginx", show_output=show)
