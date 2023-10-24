# Overlord library
from web.settings import PUBLIC_KEY
from core.library import api, JsonResponse, console
from core.tools.tools import run


def external_command(req, *args, **kwargs) -> JsonResponse:
  """
  Allows users to interact with the Overlord CLI for this project remotely.

  :param req obj: request object from the browser
  :return output: reference the output function
  """
  try:
    # Acquire request data
    json = api.get_json(req)
    pub_key = json['pub_key'] if 'pub_key' in json else None
    cmd_line = json['cmd_line'] if 'cmd_line' in json else None

    # Authenticate user
    if not pub_key == PUBLIC_KEY or PUBLIC_KEY is None or PUBLIC_KEY == '':
      return api.fail("Failed to authenticate user.")

    # Verify command
    if cmd_line is None or len(cmd_line) == 0:
      return api.fail("No command line was provided.")

    # Execute command
    run(set_command_line=cmd_line)
    return api.data({
      "message": "Successfully executed command.",
      "output": console.__log_cache__
    })

  except Exception as exec_error:
    return api.fail(str(exec_error))
