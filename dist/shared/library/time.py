from django.utils import timezone
from datetime import datetime as _datetime


def encoded(datetime:_datetime|None = None, include_seconds:bool = False) -> str:
  datetime_obj = _datetime.now(tz=timezone.utc) if datetime is None else datetime
  if include_seconds:
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
  return datetime_obj.strftime("%Y-%m-%dT%H:%M:00.0Z")


def timestamp(datetime:_datetime|None = None, include_time=True) -> str:
  _date, _time = datetime(datetime, True).split('T')
  _time = _time.split('.')[0]
  _date = _date.split('-')
  _date = f"{_date[2]}/{_date[1]}/{_date[0]}"
  if include_time:
    return f"{_date} {_time}"
  return f"{_date}"


def now() -> _datetime:
  return _datetime.now(tz=timezone.utc)
