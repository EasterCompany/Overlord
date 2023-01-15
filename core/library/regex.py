# Standard library
import re


def to_alphanumeric(string:str, hyphens_to_underscores=True) -> str:
  """
  Purges any non-alphanumeric characters from a string and optionally
  converts hyphens to underscores

  :param string str: the sample text
  :return str: alphanumeric string
  """
  if hyphens_to_underscores:
    string = string.replace('-', '_')
  return re.sub(r'[\W]+', '', string)


def is_alphanumeric(string:str) -> bool:
  """
  Indicates whether a string only contains alphanumeric characters

  :param string str: the sample text
  :return bool: true if the string only contains alphanumeric characters
  """
  return string == to_alphanumeric(string, hyphens_to_underscores=True)
