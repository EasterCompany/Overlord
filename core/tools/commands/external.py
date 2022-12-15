# Overlord library
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
    command = api.get_json(req)['command']

    if command == 'deploy':
      git.pull.all()
      return output('Server deployment executed successfully')

    return output(
      f'''USER: {user[0]}\n\nSESSION: {user[1]}\n\nCOMMAND: {command}'''
    )

  except Exception as exception:
    return output(str(exception))
