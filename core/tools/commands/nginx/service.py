from core.library import console
from web.settings import PROJECT_NAME

stop = lambda show=True: console.sudo("systemctl stop nginx", show_output=show)
start = lambda show=True: console.sudo("systemctl start nginx", show_output=show)
restart = lambda show=True: console.sudo("systemctl restart nginx", show_output=show)
reload = lambda show=True: console.sudo("systemctl daemon-reload", show_output=show)

stop_app = lambda show=True: console.sudo(f"systemctl stop {PROJECT_NAME}", show_output=show)
start_app = lambda show=True: console.sudo(f"systemctl start {PROJECT_NAME}", show_output=show)
restart_app = lambda show=True: console.sudo(f"systemctl restart {PROJECT_NAME}", show_output=show)
