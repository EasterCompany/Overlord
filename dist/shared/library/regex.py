import re as _re


def to_alphanumeric(string:str, hyphens_to_underscores=True) -> str:
  '''
  Purges any non-alphanumeric characters from a string and optionally
  converts hyphens to underscores
  '''
  if hyphens_to_underscores:
    string = string.replace('-', '_')
  return _re.sub(r'[\W]+', '', string)


def is_alphanumeric(string:str) -> bool:
  ''' Indicates whether a string only contains alphanumeric characters '''
  return string == to_alphanumeric(string, hyphens_to_underscores=True)
