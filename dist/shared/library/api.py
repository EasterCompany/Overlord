from urllib.parse import urlparse, unquote
from django.urls import path as new_path, re_path as new_re_path
from django.http import JsonResponse, HttpResponse, FileResponse
from shared.library.common import *
from shared.apps.user.models import User

OK = 'OK'
BAD = 'BAD'


def std(status:str, message:list|tuple|int|str|float|dict = "Invalid Status Response"):
  """ Standard API Response Method """
  if isinstance(message, Exception):
    message = str(message)
  return JsonResponse({
    'status': status,
    'data': message,
  })

def success() -> JsonResponse:
  """ Request was executed successfully response """
  return std(OK, "Request was executed successfully.")


def fail(message:str) -> JsonResponse:
  """ Request failed with an error message """
  return std(BAD, message)


def error(exception=None) -> JsonResponse:
  """
  Request resulted in an internal server error, that will only
  return an error message in development or staging environments
  with DEBUG mode enabled.

  In a production environment with DEBUG mode disabled, returns
  a generic '500 internal server error' response instead.
  """
  if exception is not None and settings.DEBUG:
    print(f"""
  [{console.out("INTERNAL SERVER ERROR", "red", False)}]
  {exception}
  """)
    return std(BAD, str(exception))
  return std(BAD, "[500] Internal server error.")


def data(JSON:dict) -> JsonResponse:
  """ Request has successfully produced JSON data to return to the user """
  return std(OK, JSON)


def get_arg(_arg) -> str:
  """ Unquotes an argument from the request and strips it """
  return str(unquote(_arg)).strip()


def get_user(req):
  """
  Acquires the user uuid and session token from the authorization header
  passed by api, POST & oapi client side functions
  """
  try:
    auth_token = req.headers.get('Authorization').split("[:~OLT~:]")
    uuid = auth_token[0].split('Basic ')[1].strip()
    session = "[:~OLT~:]" + auth_token[1]
    user = User(identifier=uuid)
    if user.data.session == session:
      return user
    return None
  except:
    return None


def get_body(req) -> str:
  """
  Consumes the request input and returns a decoded utf-8 string containing
  the content of the body
  """
  return req.body.decode('utf-8')


def get_json(req) -> dict:
  """
  Consumes the request input and returns a dictionary containing
  the content of the body which is expected to be stringified json
  """
  return json.loads(req.body.decode('utf-8'))


def get_decoded_base64_file(file_name:str, data:str) -> str|bytes:
  """
  Consumes base64 encoded image file from JSON or Text Data and returns
  a standard decoded image file with the appropriate extension
  """

  def get_file_extension(file_name, decoded_file):
    extension = imghdr.what(file_name, decoded_file)
    extension = "jpg" if extension == "jpeg" else extension
    return extension

  if isinstance(data, six.string_types):
    if 'data:' in data and ';base64,' in data:
      header, data = data.split(';base64,')

    try:
      decoded_file = base64.b64decode(data)
    except TypeError:
      TypeError('invalid_image')

    file_extension = get_file_extension(file_name, decoded_file)
    file_uuid = str(uuid.uuid4())[:7]
    complete_file_name = "%s.%s.%s" % (file_name, file_uuid, file_extension)
    return complete_file_name, decoded_file
