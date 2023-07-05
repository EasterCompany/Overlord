# Standard library
import six
import uuid
import json
import imghdr
import base64
from urllib import parse
# Overlord library
from web.settings import DEBUG
from django.urls import path as new_path
from django.http import JsonResponse
from core.library import console

OK = 'OK'
BAD = 'BAD'


# Overlord Standard Response Function ----------------------------------------------------------------------------------
def std(status:str, message:list|tuple|int|str|float|dict = "Invalid Status Response"):
  """
  Standard API Response Method

  :param status (OK/BAD): api.OK or api.BAD type
  :param message dict: contains api response data
  :return dict: {status, message}
  """
  if isinstance(message, Exception):
    message = str(message)
  return JsonResponse({
    'status': status,
    'data': message,
  })


# Overlord API Specific Response Types ---------------------------------------------------------------------------------
def success() -> JsonResponse:
  ''' Request was executed successfully response '''
  return std(OK, "Request was executed successfully.")


def fail(message:str) -> JsonResponse:
  ''' Request was denied or failed to execute '''
  return std(BAD, message)


def error(exception=None) -> JsonResponse:
  """
  Internal server error standard response method

  :param exception str: message caught upon error exception
  :return: api.std showing a HTTP 500 Error
  """
  if exception is not None and DEBUG:
    print(f"""
  [{console.out("INTERNAL SERVER ERROR", "red", False)}]
  {exception}
  """)
    return std(BAD, str(exception))
  return std(BAD, "[500] Internal server error.")


def data(JSON:dict) -> JsonResponse:
  """
  Request has successfully produced data to return to the user

  :param JSON dict: usually a dictionary containing fields and values
  :return: api.std with OK status and dictionary as the message parameter.
  """
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
  """
  Unquotes an argument from the request and strips it

  :param _arg str: any string
  :return str: unquoted and stripped string
  """
  return str(parse.unquote(_arg)).strip()


def get_user(req) -> tuple:
  """
  Acquires the user uuid and session token from the authorization header
  passed by api, POST & xapi client side functions

  :param req obj: default django request object
  :return list: [ user_uuid, user_token ]
  """
  try:
    auth_token = req.headers.get('Authorization').split("[:~OLT~:]")
    return auth_token[0].split('Basic ')[1].strip(), auth_token[1]
  except:
    return '', ''


def get_body(req) -> str:
  """
  Consumes the request input and returns a decoded utf-8 string containing
  the content of the body

  :param req obj: default django request object
  :return str: body content
  """
  return req.body.decode('utf-8')


def get_json(req) -> dict:
  """
  Consumes the request input and returns a dictionary containing
  the content of the body which is expected to be stringified json

  :param req obj: default django request object
  :return dict: body content as json
  """
  return json.loads(req.body.decode('utf-8'))


def get_decoded_base64_file(file_name:str, data:str) -> str|bytes:

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

  # API.NAME records the interface name for this new api
  NAME:str|None = None

  # API.CLIENT_NAME records the client related to this api
  CLIENT_NAME:str|None = None

  def __init__(self) -> None:
    self.URLS = []

  def abspath(self,
    endpoint:str, view, prefix:str|None = None,
    description:str = "Auto Generated Absolute Path",
    *args, **kwargs
  ):
    _path = f"{self.CLIENT_NAME}/{endpoint}" if prefix == "client" else \
      f"{self.NAME}/{endpoint}" if prefix == "name" else f"{endpoint}"
    return self.URLS.append(new_path(_path, view, name=description))

  def path(self, endpoint, view, description="Auto Generated Path", *args, **kwargs):
    if self.NAME is None:
      _path = f"api/{endpoint}"
    else:
      _path = f"api/{self.NAME}/{endpoint}"
    return self.URLS.append(
      new_path(_path, view, name=description)
    )
