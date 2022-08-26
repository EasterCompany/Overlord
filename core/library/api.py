# Standard library
from urllib import parse
# Django library
from django.http import JsonResponse
# Overlord library
from web.settings import DEBUG
from .console import Console

OK = 'OK'
BAD = 'BAD'
CON = Console()


# Overlord Standard Response Function ----------------------------------------------------------------------------------


def std(status, message="Invalid Status Response"):
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


def success():
  """
  Request was executed successfully response

  :return: api.std showing a HTTP 200 Success
  """
  return std(OK, "Request was executed successfully.")


def error(exception=None):
  """
  Internal server error standard response method

  :param exception str: message caught upon error exception
  :return: api.std showing a HTTP 500 Error
  """
  if exception is not None and DEBUG:
    print(f"""
      [{CON.output("INTERNAL SERVER ERROR", "red")}]

    {exception}
    """)
  return std(BAD, "[500] Internal server error.")


def data(JSON):
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


def get_arg(_arg):
  """
  Unquotes an argument from the URI and strips it

  :param _arg str: any string
  :return str: unquoted and stripped string
  """
  return parse.unquote(_arg).strip()


def get_user(req):
  """
  Acquires the user uuid and session token from the authorization header
  passed by api, POST & xapi the JS functions

  :param req obj: default django request object
  :return list: [ user_uuid, user_token ]
  """
  auth_token = req.headers.get('Authorization').split("[:~OLT~:]")
  return auth_token[0].split('Basic ')[1].strip(), auth_token[1]


def get_body(req):
  return req.body.decode('utf-8')
