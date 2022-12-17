# Standard library
import subprocess
from sys import executable
# Overlord library
from web.settings import PUBLIC_KEY, BASE_DIR
from core.library import api, JsonResponse
from core.tools.commands import git, django, node, pa


def OK():
  return output("<b>STATUS:</b> <i style='color:green;'>OK</i>")


def upgrade():
  git.pull.all()
  subprocess.call(f"{executable} -m pip install -r requirements.txt", shell=True, cwd=True)
  return OK()


def reload_server():
  pa.reload.request()
  return output("<i style='color:yellow;'>Service may be interrupted while reloading, please wait...</i>")


def deploy():
  upgrade()
  django.server.migrate_database()
  reload_server()
  return output(
    "Successfully upgraded server\n"
    "<i style='color:yellow;'>Service may be interrupted while reloading, please wait...</i>"
  )


def build():
  node.clients.build_all()
  return output("<i style='color:green;'>Successfully built all clients!</i>")


def output(message:str) -> JsonResponse:
  """
  Standardised response message for useCommandExtension functions

  :param message str: what response is printed in the web console
  :return JsonResponse: message within an standardised object
  """
  return api.data({ 'output': message })


def external_command(req, *args, **kwargs):
  """
  Framework function for calling commands to the Overlord Server
  externally, such as from an E-Panel web console

  :param req obj: request object from the browser
  :return output: reference the output function
  """
  try:
    json = api.get_json(req)
    command = json['command'] if 'command' in json else None
    pub_key = json['pub_key'] if 'pub_key' in json else None

    # Authenticate request
    if pub_key == PUBLIC_KEY and PUBLIC_KEY is not None and PUBLIC_KEY != '': pass
    else:
      return api.error("Failed to Authentication User")

    # Check for commands matching input
    if command in commands:
      try:
        return commands[command]()
      except Exception as exec_error:
        return output(str(exec_error))

    # No command executed
    return output(f"[ERROR] No command matching '{command}'")

  except Exception as exception:
    return api.error(str(exception))


# External Command Input List
commands = {
  "status": OK,
  "upgrade": upgrade,
  "reload": reload_server,
  "deploy": deploy,
  "build": build,
  "migrate": django.server.migrate_database
}
