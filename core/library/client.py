# Standard library
from wsgiref.util import FileWrapper
# Overlord library
from web import settings
from core.library import (
  HttpResponse,
  re_path,
  render,
  html_loader,
  path as new_path,
  local_ip
)

# Random Ports Used Counter
_RPU = 0


def RPU():
  '''
  Global function for acquiring a random port to assign to any Overlord FE hosted client.

  :return str: Integer value represented as a string to preserve prefixed zeros.
  '''
  global _RPU
  _CACHE = _RPU
  _RPU = _CACHE + 1
  return 8199 - _RPU


class WebClient():
  '''
  Server Configuration for any Create-React-App based Client.

  Settings will be loaded initially; then we will load the
  Web-Client with consideration for configuration for
  either local development, staging or production environments.

  The .env file will be overwritten when the application loads
  so any configuration which require modification to this file
  should be done here.

  [SPACES ARE PURGED FROM CONFIGURATION SETTINGS IN THE ENV FILE]
  '''

  # Client.ENVIRONMENT [ local, staging, production... ]
  ENV:str = __file__.replace('__init__.py', '.env')

  # Client.DIR represents which sub-directory inside the 'clients/'
  # directory contains the source code for this client
  DIR:str = str()

  # Client.URLS records custom endpoints added by the client relative to
  # the clients own endpoint
  URLS:list|None = []

  # Client.URLS_re_paths records the custom endpoints added by the client
  # in an r string so that the app file ignores those endpoints
  URLS_re_paths:str = r""

  # Client.NAME represents what the stylized name of this client should be
  # for example; this is often used to set the HTML <title> element content
  NAME:str = DIR

  # Client.PORT by default will be automatically determined if PORT is None.
  # otherwise you can specify a port number as a string.
  PORT:int|None = RPU()

  # Client.DEV_PORT is an overridable variable which tells the client which
  # port the API is accessible on when in a development environment
  DEV_PORT:str = settings.SECRET_DATA['LOCAL_PORT']

  # Client.ENDPOINT controls which `base url` will host your application
  # By default, only the INDEX client can connect to the root (http..com/) url
  # Also, all paths beginning with this ENDPOINT will instead be forwarded to
  # this application - this is why we give the INDEX setting special treatment.
  ENDPOINT:str = NAME if not NAME == settings.INDEX else ''

  # Client.IS_INDEX is a boolean which indicates weather or not this client
  # is the index client hosted on the root of the domain
  IS_INDEX:bool = NAME == settings.INDEX

  # Client.API is a string representing which endpoint to connect to when making API
  # requests. By default, `http../api` will be used if API is set to `None`
  API:str|None = None

  # Client.PWA is a boolean which indicates whether or not to enable service workers
  PWA:bool = False

  # Client.__context__ is an overridable function which will be called to serve your
  # react application. URL parameters are passed as parameters to this function.
  __context__ = None

  # Client.__urls__ is an overridable function which will be called when generating
  # the urls for this client, it can provide additional urls outside of the basic
  # react web app functionalities.
  __urls__ = None

  # Client.is_native is an non-overridable variable which indicates weather or not
  # this client is a react-native based client or not.
  is_native:bool = False

  def __init__(self):
    # User setup dependent options
    if self.DIR is None:
      self.DIR = self.NAME
    if self.ENDPOINT == '':
      self.ENDPOINT = self.DIR if not self.DIR == settings.INDEX else ''
    self.IS_INDEX = self.ENDPOINT == ''
    # Generate production environment file
    with open(self.ENV, 'w') as prd_env:
      prd_env.write(self._env(prd=True if not self.is_native else not settings.DEBUG))
    if not self.is_native:
      # Generate development environment file
      with open(self.ENV + '.dev', 'w') as dev_env:
        dev_env.write(self._env(prd=False))
    # Build the url structure
    self.URL = self._url()
    self.URLS = self.__urls__() if callable(self.__urls__) else None
    # Load HTML Template
    self.html = None
    self.html_path = f'{self.DIR}.app'

  def _url(self):
    ''' Client._url is a re_path pointing towards the clients app file '''
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
    return re_path(re_path_str, self.app, name=f"{self.NAME} App")

  def _env(self, prd=True):
    '''
    Generate Client Environment Configuration

    Creates the .env file for this client on this environment which
    automatically adjusts between local development, staging or production
    '''
    if self.PORT is None:
      self.PORT = RPU()
    api = self.API if self.API is not None else f'api/{self.DIR}/'
    pwa = 'true' if self.PWA else 'false'
    dev_url = f"/{self.ENDPOINT}/" if len(self.ENDPOINT) > 0 else "/"

    if prd: return f'''# .env
    #   automatically generated file
    #   do not edit or delete
    PORT={self.PORT}
    BUILD_PATH={settings.BASE_DIR + '/static/' + self.DIR}
    PUBLIC_URL=/static/{self.DIR}/
    REACT_APP_ENV=Prd
    REACT_APP_NAME={self.NAME}
    REACT_APP_API={api}
    REACT_APP_PWA={pwa}
    REACT_APP_STATIC=/static/{self.DIR}/
    REACT_APP_ENDPOINT={self.ENDPOINT}
    REACT_APP_IS_INDEX={str(self.IS_INDEX).lower()}
    '''.replace('    ', '')

    return f'''# .env.dev
    #   automatically generated file
    #   do not edit or delete
    PORT={self.PORT}
    BUILD_PATH={settings.BASE_DIR + '/static/' + self.DIR}
    PUBLIC_URL={dev_url}
    REACT_APP_ENV=Dev
    REACT_APP_NAME={self.NAME}
    REACT_APP_API={api}
    REACT_APP_PWA={pwa}
    REACT_APP_STATIC={dev_url}
    REACT_APP_ENDPOINT={self.ENDPOINT}
    REACT_APP_IS_INDEX={str(self.IS_INDEX).lower()}
    REACT_APP_DEV_PORT={self.DEV_PORT}
    '''.replace('    ', '')

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


class NativeClient(WebClient):
  '''
  Server Configuration for a React-Native based Client.

  Settings will be loaded initially; then we will load the
  Native-Client with consideration for configuration for
  either local development, staging or production environments.

  The .env file will be overwritten when the application loads
  so any configuration which require modification to this file
  should be done here.

  [SPACES ARE PURGED FROM CONFIGURATION SETTINGS IN THE ENV FILE]
  '''

  # Client.API_DOMAIN is an overridable variable which tells the client where
  # the api will be hosted in production. This is essential for native clients
  # as they won't have a relative domain to access when deployed to Android/iOS.
  API_DOMAIN:str = f"http://{local_ip}:{settings.SECRET_DATA['LOCAL_PORT']}"

  # Client.DEV_PORT is an overridable variable which tells the client which
  # port the API is accessible on when in a development environment
  DEV_PORT:str = settings.SECRET_DATA['LOCAL_PORT']

  # Client.is_native is an non-overridable variable which indicates weather or not
  # this client is a react-native based client or not.
  is_native:bool = True

  def _env(self, prd=True):
    '''
    Generate Client Environment Configuration

    Creates the .env file for this client on this environment which
    automatically adjusts between development & production configurations
    '''
    if self.PORT is None:
      self.PORT = RPU()
    api = self.API if self.API is not None else f'api/{self.DIR}/'
    pwa = 'true' if self.PWA else 'false'
    dev_url = f"/{self.ENDPOINT}/" if len(self.ENDPOINT) > 0 else "/"

    if prd: return f'''# .env
    #   automatically generated file
    #   do not edit or delete
    API_DOMAIN={self.API_DOMAIN}
    PUBLIC_URL=
    REACT_APP_ENV=Prd
    REACT_APP_NAME={self.NAME}
    REACT_APP_API={api}
    REACT_APP_PWA={pwa}
    REACT_APP_STATIC=/static/{self.DIR}/
    REACT_APP_ENDPOINT={self.ENDPOINT}
    REACT_APP_IS_INDEX={str(self.IS_INDEX).lower()}
    '''.replace('    ', '')

    return f'''# .env.dev
    #   automatically generated file
    #   do not edit or delete
    API_DOMAIN=http://{local_ip}:{settings.SECRET_DATA['LOCAL_PORT']}
    PUBLIC_URL={dev_url}
    REACT_APP_ENV=Dev
    REACT_APP_NAME={self.NAME}
    REACT_APP_API={api}
    REACT_APP_PWA={pwa}
    REACT_APP_STATIC={dev_url}
    REACT_APP_ENDPOINT={self.ENDPOINT}
    REACT_APP_IS_INDEX={str(self.IS_INDEX).lower()}
    REACT_APP_DEV_PORT={self.DEV_PORT}
    '''.replace('    ', '')
