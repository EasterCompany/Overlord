# Standard library
from datetime import datetime as _datetime
from django.utils import timezone


def get_datetime_string(datetime:_datetime|None = None, include_seconds:bool = False) -> str:
  """
  Get a standardised date time string, by default the string contains the current datetime,
  however if a datetime object is provided it will be a stringified datetime string of that
  datetime object.

  This method is good when using datetime columns in a database and will be readable by the
  computer.

  :param datetime obj: a datetime object (current time if None)
  :param include_seconds bool: weather or not to count the seconds (0.0 seconds if False)
  :return str: string containing a formatted ISO timestamp
  """
  datetime_obj = _datetime.now(tz=timezone.utc) if datetime is None else datetime
  if include_seconds:
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
  return datetime_obj.strftime("%Y-%m-%dT%H:%M:00.0Z")


def timestamp(datetime:_datetime|None = None, include_time=True, gb_format=False) -> str:
  """
  Creates a simple human readable timestamp, this method is good for prepending logs and
  other output which is primarily for users to read.

  :return str: string containing timestamp
  """
  _date, _time = get_datetime_string(datetime, True).split('T')
  _time = _time.split('.')[0]
  if gb_format:
    _date = _date.split('-')
    _date = f"{_date[2]}/{_date[1]}/{_date[0]}"
  if include_time:
    return f"{_date} {_time}"
  return f"{_date}"


def now() -> _datetime:
  return _datetime.now(tz=timezone.utc)
