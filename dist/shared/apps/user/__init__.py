from shared.library import app, settings, common

class USER(app.App):
  ENV:str = __file__.replace('__init__.py', '.env')
  DIR:str = common.path(__file__).absolute_parent
  PWA:bool = True
  PWA_URL:str = "https://easter.company/user"
  DISABLED:bool = False

  NAME = "user"
  name = "user"
  IS_INDEX = False
  ENDPOINT = "user"

  LOCAL_PROTOCOL:str|None = None if (not settings.DEBUG) else \
    "http"
  LOCAL_IP:str|None = None if (not settings.DEBUG) else \
    f"{common.get_local_ip()}"
  LOCAL_PORT:str|None = None if (not settings.DEBUG) else \
    settings.LOCAL_PORT
  LOCAL:str|None = None if (not settings.DEBUG) else \
    f"{LOCAL_PROTOCOL}{LOCAL_IP}{LOCAL_PORT}" if not settings.DEBUG else None
