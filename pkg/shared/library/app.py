from shared.library.common import (
  settings, new_path, new_re_path, path,
  html_loader, HttpResponse, JsonResponse, FileWrapper, FileResponse, render,
)

class App:
  ENV:str = __file__.replace('__init__.py', '.env')
  DIR:str = path(__file__).absolute_parent
  PWA:bool = True
  PWA_URL:str = ""
  DISABLED:bool = False

  NAME:str = DIR
  name:str = DIR.lower()
  IS_INDEX:bool = (NAME == settings.INDEX) and not DISABLED
  ENDPOINT:str = '' if IS_INDEX else (name if not DISABLED else f"/olt/disabled/{name}")

  LOCAL_PROTOCOL:str|None = None if (not settings.DEBUG) else \
    settings.LOCAL_PROTOCOL
  LOCAL_IP:str|None = None if (not settings.DEBUG) else \
    settings.LOCAL_IP
  LOCAL_PORT:str|None = None if (not settings.DEBUG) else \
    settings.LOCAL_PORT
  LOCAL:str|None = None if (not settings.DEBUG) else \
    f"{LOCAL_PROTOCOL}{LOCAL_IP}{LOCAL_PORT}" if not settings.DEBUG else None

  REMOTE_PROTOCOL:str|None = None if (settings.DEBUG or DISABLED) else \
    settings.REMOTE_PROTOCOL
  REMOTE_IP:str|None = None if (settings.DEBUG or DISABLED) else \
    settings.REMOTE_IP
  REMOTE_PORT:str|None = None if (settings.DEBUG or DISABLED) else \
    settings.REMOTE_PORT
  REMOTE_API:str|None = None if (settings.DEBUG or DISABLED) else \
    f"{REMOTE_PROTOCOL}{REMOTE_IP}{REMOTE_PORT}/api/{name}"
  REMOTE_CLIENT:str|None = None if (settings.DEBUG or DISABLED) else \
    f"{REMOTE_PROTOCOL}{REMOTE_IP}{REMOTE_PORT}{ENDPOINT}"

  URLS:list = []
  URLS_re_paths:str = r""
  SOCKETS:list = []

  def __init__(self) -> None:
    pass

  def __urls__(self) -> list:
    return []

  def __context__(self) -> dict:
    return {
      "NAME": self.NAME,
      "ENDPOINT": self.ENDPOINT,
      "IS_INDEX": self.IS_INDEX,
      "PWA": self.PWA,
      "DISABLED": self.DISABLED,
    }

  def __env__(self):
    ''' Generate the client's environment variables '''
    pwa = 'true' if self.PWA else 'false'
    dev_url = f"/{self.ENDPOINT}/" if len(self.ENDPOINT) > 0 else "/"
    return f'''
    API_URL={self.API_URL}
    PUBLIC_URL={dev_url if settings.DEBUG else ''}
    REACT_APP_ENV={'Dev' if settings.DEBUG else 'Prd'}
    REACT_APP_DIR={self.DIR}
    REACT_APP_PWA={pwa}
    REACT_APP_NAME={self.NAME}
    REACT_APP_API_URL={self.API_URL}
    REACT_APP_API_PORT={self.API_PORT}
    REACT_APP_STATIC=/static/{self.DIR}/
    REACT_APP_ENDPOINT={self.ENDPOINT}
    REACT_APP_IS_INDEX={str(self.IS_INDEX).lower()}
    '''.replace('    ', '')

  def _url(self):
    ''' Client._url is a re_path pointing towards the clients app file '''
    if self.DISABLED:
      return
    def_str = \
      r"^(?!static)^(?!api)^(?!robots.txt)^(?!manifest.json)^(?!asset-manifest.json)^(?!favicon.ico)^(?!sitemap.xml)"
    pwa_str = \
      r"^(?!service-worker.js)^(?!service-worker.js.map)"
    app_str = \
      r".*$"
    if self.PWA:
      re_path_str = def_str + self.URLS_re_paths + pwa_str + app_str
    else:
      re_path_str = def_str + self.URLS_re_paths + app_str
    return new_re_path(re_path_str, self.app)

  def _env(self, prd=True):

  def _path(self, file_name):
    '''
    Use this function to get the raw string containing the complete path
    for the file you would like to serve.
    '''
    return settings.BASE_DIR + f"/static/{self.DIR}/{file_name}"

  def path(self, endpoint:str, view, description:str = "Auto Generated Path", *args, **kwargs):
    ''' Creates a new endpoint associated with this client '''
    _path = f"{self.DIR}/{endpoint}" if not self.IS_INDEX else f"{endpoint}"
    self.URLS_re_paths += rf"^(?!{endpoint})"
    if not self.DISABLED:
      return new_path(_path, view, name=description)

  def current_uri(self, req) -> str:
    ''' Returns the current url including any queries '''
    return req.build_absolute_uri('?')

  def current_url(self, req) -> str:
    ''' Returns the current url '''
    return req.build_absolute_uri('?')

  def current_domain(self, req) -> str:
    ''' Returns the current domain name and protocol as a string '''
    return req.build_absolute_uri('/').strip('/')

  def current_path(self, req) -> list:
    ''' Returns the current path from the url '''
    return req.build_absolute_uri('?').replace(self.current_domain(req), '').strip('/').split('/')

  def current_view(self, req) -> str:
    ''' Returns the last item from the url path list as a string '''
    return req.build_absolute_uri('?').split('/')[-1]

  def render_html(self, req, context:dict) -> HttpResponse:
    ''' Renders the default HTML file with a given context parameter '''
    if self.html is None:
      self.html = html_loader.get_template(self.html_path)
    return HttpResponse(self.html.render(context, req), content_type="text/html")

  def app(self, req, *args, **kwargs):
    ''' Renders the main app file as HTML with or without provided contexts '''
    if self.__context__ is not None and callable(self.__context__):
      return self.render_html(req, self.__context__(req))
    return render(req, self._path(self.html_path), content_type='text/html')

  def favicon(self, req, *args, **kwargs):
    ''' Renders the associated client favicon '''
    return self.serve_file('favicon.ico')(req, *args, **kwargs)

  def sitemap(self, req, *args, **kwargs):
    ''' Renders the associated client sitemap file '''
    return render(req, self._path('sitemap.xml'), content_type='text/html')

  def robots(self, req, *args, **kwargs):
    ''' Renders the associated client robots file '''
    return render(req, self._path('robots.txt'), content_type='text/plain')

  def manifest(self, req, *args, **kwargs):
    ''' Renders the associated client manifest file '''
    return render(req, self._path('manifest.json'), content_type='application/json')

  def assets(self, req, *args, **kwargs):
    ''' Renders the associated client asset manifest file '''
    return render(req, self._path('asset-manifest.json'), content_type='application/json')

  def service_worker(self, req, *args, **kwargs):
    ''' Renders the associated client service worker file '''
    return render(req, self._path('service-worker.js'), content_type='application/x-javascript')

  def service_worker_map(self, req, *args, **kwargs):
    ''' Renders the associated client service worker map file '''
    return render(req, self._path('service-worker.js.map'), content_type='application/x-javascript')

  def serve_file(self, path:str, abspath:bool=False):
    '''
    Loads a file into memory and then serves it with the appropriate mime type in an http response

    :param path str: usually a relative path to a file from within the public directory of the client
    :param abspath bool: indicates that the path parameter is an absolute path to anywhere on the system
    :return HttpResponse:
    '''
    _bytes = open(path if abspath else self._path(path), "rb")
    _file = FileWrapper(_bytes)
    mime_type = None
    if path.endswith('.mp4'):
      mime_type = 'video/mp4'
    elif path.endswith('.mp3'):
      mime_type = 'audio/mp3'
    elif path.endswith('.ico'):
      mime_type = 'image/x-icon'
    elif path.endswith('.png'):
      mime_type = 'image/png'
    elif path.endswith('.jpg'):
      mime_type = 'image/jpeg'
    elif path.endswith('.svg'):
      mime_type = 'image/svg+xml'
    elif path.endswith('.cur'):
      mime_type = 'image/x-win-bitmap'
    elif path.endswith('.wasm'):
      mime_type = 'application/wasm'
    elif path.endswith('.js'):
      mime_type = 'application/x-javascript'
    elif path.endswith('.json'):
      mime_type = 'application/json'
    elif path.endswith('.css'):
      mime_type = 'text/css'
    elif path.endswith('.txt'):
      mime_type = 'text/plain'
    elif path.endswith('.xml'):
      mime_type = 'text/xml'
    elif path.endswith('.html'):
      mime_type = 'text/html'
    elif path.endswith('.woff'):
      mime_type = 'font/woff'
    elif path.endswith('.ttf'):
      mime_type = 'font/ttf'
    elif path.endswith('.eot'):
      mime_type = 'font/eot'
    return lambda req, *args, **kwargs: HttpResponse(_file, content_type=mime_type)

  def abs_api_path(self, endpoint:str, view, prefix:str|None = None) -> None:
    _path = f"{self.CLIENT_NAME}/{endpoint}" if prefix == "client" else \
      f"{self.NAME}/{endpoint}" if prefix == "name" else f"{endpoint}"
    return self.URLS.append(new_path(_path, view))

  def api_path(self, endpoint:str, view, *args, **kwargs) -> None:
    if self.NAME is None:
      _path = f"api/{endpoint}"
    else:
      _path = f"api/{self.NAME}/{endpoint}"
    return self.URLS.append(new_path(_path, view))

  def socket(self, endpoint:str, view, *args, **kwargs) -> None:
    if self.NAME is None:
      _path = f"ws/{endpoint}"
    else:
      _path = f"ws/{self.NAME}/{endpoint}"
    self.URLS.append(new_re_path(_path, view.as_asgi()))
