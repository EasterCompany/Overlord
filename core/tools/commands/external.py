# Overlord library
from web.settings import PUBLIC_KEY
from core.library import api, JsonResponse
from core.tools.commands import git


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
    user = api.get_user(req)
    json = api.get_json(req)
    command = json['command'] if 'command' in json else None
    pub_key = json['pub_key'] if 'pub_key' in json else None

    # Authenticate User via Public Key Method
    if pub_key == PUBLIC_KEY and PUBLIC_KEY is not None and PUBLIC_KEY != '': pass
    # TODO: Authenticate User via User Session Method
    # elif ...
    else:
      return api.error("Failed to Authentication User")

    if command == 'deploy':
      git.pull.all()
      return output('Server deployment executed successfully')

    return api.error()
  except Exception as exception:
    return api.error(str(exception))
