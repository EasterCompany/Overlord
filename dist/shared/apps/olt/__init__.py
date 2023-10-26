from shared.library import api

class _API(api.UniversalAPI):
  NAME = "olt"

  def __init__(self) -> None:
    super().__init__()

OLT = _API()
