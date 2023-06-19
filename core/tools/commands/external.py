# Overlord library
from web.settings import PUBLIC_KEY
from core.library import api, JsonResponse
from core.tools.commands import git, django, pa


def OK() -> JsonResponse:
  """
  Used as a standard 'OK' response for external command requests
  """
  return output("<b>STATUS:</b> <i style='color:green;'>OK</i>")


def upgrade() -> JsonResponse:
  """
  Pulls new code from the current branch origin and then installs
  any new server dependencies from the 'core/requirements.txt' file
  """
  git.pull.all()
  django.server.install_requirements()
  django.server.migrate_database()
  return OK()


def reload_server() -> JsonResponse:
  """
  Requests that the server API reload the server instance
  """
  pa.reload.request()
  return output("<i style='color:yellow;'>Service may be interrupted while reloading, please wait...</i>")


def deploy() -> JsonResponse:
  """
  upgrade & reload the server instance in that specific order
  """
  upgrade()
  reload_server()
  return output(
    "Successfully upgraded server\n"
    "<i style='color:yellow;'>Service may be interrupted while reloading, please wait...</i>"
  )


def output(message:str) -> JsonResponse:
  """
  Standardised response message for external command functions

  :param message str: what response is printed in the web console
  :return JsonResponse: message within an standardised object
  """
  return api.data({ 'output': message })


def external_command(req, *args, **kwargs) -> JsonResponse:
  """
  Framework function for calling commands to the Overlord Server
  externally, such as from an E-Panel web console

  :param req obj: request object from the browser
  :return output: reference the output function
  """
  try:
    # Acquire request data
    json = api.get_json(req)
    command = json['command'] if 'command' in json else None
    pub_key = json['pub_key'] if 'pub_key' in json else None
    arguments = json['arguments'] if 'arguments' in json else None

    # Authenticate request
    if pub_key == PUBLIC_KEY and PUBLIC_KEY is not None and PUBLIC_KEY != '':
      pass
    else:
      return api.error("Failed to Authentication User")

    # Check for commands matching input
    if command in commands:
      try:
        if arguments is None:
          # Execute command without arguments
          return commands[command]()
        # Execute command with arguments
        return commands[command](*arguments)
      except Exception as exec_error:
        # Command executed with error
        return output(str(exec_error))
    # No command executed
    return output(f"[ERROR] No command matching '{command}'")
  # Encountered unexpected error
  except Exception as exception:
    return api.error(str(exception))


# External command options
commands:dict = {
  "status": OK,
  "upgrade": upgrade,
  "reload": reload_server,
  "deploy": deploy
}
