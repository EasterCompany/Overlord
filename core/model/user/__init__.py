"""

  Overlord Universal API Interface
  Version: 1.2.0

  Used to control and configure the default behaviour
  of an Overlord based API by changing the values of
  the variables already defined for you below

"""
from core.library.api import UniversalAPI


class _API(UniversalAPI):

  # API.NAME [ usually dictates the origin of endpoints ]
  NAME = "user"

  # API.CLIENT_NAME [ dictates that this api belongs to a specific client ]
  CLIENT_NAME = None

  # INITIALIZE API CONFIGURATION
  def __init__(self) -> None:
    super().__init__()


# EXPORT THE INITIALIZED API OBJECT
API = _API()
