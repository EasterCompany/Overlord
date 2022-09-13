from core.library.api import UniversalAPI


class _API(UniversalAPI):

  # API.NAME [ usually dictates the origin of endpoints ]
  NAME = "recipe"

  # API.CLIENT_NAME [ dictates that this api belongs to a specific client ]
  CLIENT_NAME = None

  # INTIALIZE API CONFIGURATION
  def __init__(self) -> None:
    super().__init__()


# EXPORT THE INITIALIZED API OBJECT
API = _API()
