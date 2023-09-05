# Standard library
import six
import uuid
import json
import imghdr
import base64
from urllib import parse
# Overlord library
from django.http import JsonResponse
from django.urls import path as new_path, re_path as new_re_path
from web.settings import DEBUG
from core.library import console

OK = 'OK'
BAD = 'BAD'


# Overlord Standard Response Function ----------------------------------------------------------------------------------
def std(status:str, message:list|tuple|int|str|float|dict = "Invalid Status Response"):
  """ Standard API Response Method """
  if isinstance(message, Exception):
    message = str(message)
  return JsonResponse({
    'status': status,
    'data': message,
  })


# Overlord API Specific Response Types ---------------------------------------------------------------------------------
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
  if exception is not None and DEBUG:
    print(f"""
  [{console.out("INTERNAL SERVER ERROR", "red", False)}]
  {exception}
  """)
    return std(BAD, str(exception))
  return std(BAD, "[500] Internal server error.")


def data(JSON:dict) -> JsonResponse:
  """ Request has successfully produced JSON data to return to the user """
  return std(OK, JSON)


def table(Table, Headers, Body, filter={ "order_by": str() }):
  """
  Create a API for Populating Tables Method

  :param Table model: Model class to fetch data from
  :param headers list: list of strings containing table headers which you want to fetch and return
  return dict: api.std response
  """
  row_count = Table.objects.count()

  if row_count >= 1:

    if row_count > 100:
      row_count = 100

    body_query = Table.objects.filter().order_by(filter['order_by'])[:row_count]
    body_row_data = Body(body_query)

    return std(OK, {
      'head': Headers,
      'body': body_row_data
    })

  return std(OK, {'head': [], 'body': [ [] ]})


# Overlord API View Tools ----------------------------------------------------------------------------------------------
def get_arg(_arg) -> str:
  """ Unquotes an argument from the request and strips it """
  return str(parse.unquote(_arg)).strip()


def get_user(req):
  """
  Acquires the user uuid and session token from the authorization header
  passed by api, POST & oapi client side functions
  """
  from core.model.user.tables import User
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


# ePanel support functions --------------------------------------------------------------------------------------------
def get_api_url(panelObj) -> str:
  """
  Consumes a panel database object and returns a constructed URL that points
  towards the associated API endpoint for this panel

  :param panelObj obj: admin panel database object
  :return str: contains a complete URL
  """
  if panelObj.isWeb:
    return f"https://{panelObj.name}/{panelObj.api}/"
  return f"https://{panelObj.api}/"


# Overlord Universal API Controller Class ------------------------------------------------------------------------------
class UniversalAPI:
  """
  Server Configuration for any Overlord based API.

  This class contains all the data for a single Universal API
  which is used to configure and control the endpoints hosted
  by that API.
  """

  # API.URLS records custom endpoints added by new api
  URLS:list = []

  # API.SOCKETS records custom web sockets added by new api
  SOCKETS:list = []

  # API.NAME records the interface name for this new api
  NAME:str|None = None

  # API.CLIENT_NAME records the client related to this api
  CLIENT_NAME:str|None = None

  def __init__(self) -> None:
    self.URLS = []
    self.SOCKETS = []

  def abspath(self, endpoint:str, view, prefix:str|None = None, description:str = "Auto Generated Path") -> None:
    """ Creates a rest API endpoint without a relative path """
    _path = f"{self.CLIENT_NAME}/{endpoint}" if prefix == "client" else \
      f"{self.NAME}/{endpoint}" if prefix == "name" else f"{endpoint}"
    return self.URLS.append(new_path(_path, view, name=description))

  def path(self, endpoint:str, view, description:str = "Auto Generated Path", *args, **kwargs) -> None:
    """ Creates a rest API endpoint associated with this API """
    if self.NAME is None:
      _path = f"api/{endpoint}"
    else:
      _path = f"api/{self.NAME}/{endpoint}"
    return self.URLS.append(
      new_path(_path, view, name=description)
    )

  def socket(self, endpoint:str, view, description:str = "Auto Generated Socket", *args, **kwargs) -> None:
    """ Creates a new web socket channel associated with this API """
    if self.NAME is None:
      _path = f"api/ws/{endpoint}"
    else:
      _path = f"api/ws/{self.NAME}/{endpoint}"
    return self.SOCKETS.append(
      new_re_path(_path, view, name=description)
    )
