# Django library
from django.urls import re_path
from django.shortcuts import render

# Overlord configuration
from web import settings

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
    return str(8199 - _RPU)


class WebClient():
    '''
    Server Configuration for any Create-React-App based Client.

    Settings will be loaded initially; then we will load the
    React-Client with consideration for configuration for
    either local development, staging or production environments.

    The .env file will be overwritten when the application loads
    so any configuration which require modification to this file
    should be done here.

    [SPACES ARE PURGED FROM CONFIGURATION SETTINGS IN THE ENV FILE]
    '''

    # Client.ENVIRONMENT [ local, staging, production... ]
    ENV = ''

    # Client.NAME and directory name for this client source files should be identical
    NAME = ''

    # Client.PORT by default will be automatically determined if PORT is None.
    # otherwise you can specify a port number as a string.
    PORT = RPU()

    # Client.ENDPOINT controls which `base url` will host your application
    # By default, only the INDEX client can connect to the root (http..com/) url
    # Also, all paths beginning with this ENDPOINT will instead be forwarded to
    # this application - this is why we give the INDEX setting special treatment.
    ENDPOINT = NAME if not NAME == settings.INDEX else ''
    IS_INDEX = str(ENDPOINT == '').lower()

    # Client.API is a string representing which endpoint to connect to when making API
    # requests. By default, `http../api` will be used if API is set to `None`
    API = "api"

    # Client.PWA is a boolean which indicates whether or not to enable service workers
    PWA = False

    def __init__(self):
        # User setup dependent options
        if self.ENDPOINT == '':
            self.ENDPOINT = self.NAME if not self.NAME == settings.INDEX else ''
        self.IS_INDEX = str(self.ENDPOINT == '').lower()
        # Generate local environment file
        with open(self.ENV, '+w') as env:
            env.write(self._env())
        # Build the url structure for django
        self.URL = self._url()

    def _url(self):
        # Client.URL is a re_path pointing towards to the react index
        return re_path(r"^(?!static)^(?!assets)^(?!api).*$", self.app, name=f"{self.NAME} App")

    def _env(self):
        '''
        Generate Client Environment Configuration

        Creates the .env file for this client on this environment which
        automatically adjusts between local development, staging or production
        '''
        port = self.PORT if self.PORT is not None else RPU()
        api = self.API if self.API is not None else 'api'
        pwa = 'true' if self.PWA else 'false'

        return f'''# .env
        #   automatically generated file
        #   do not edit or delete
        PORT={port}
        PUBLIC_URL=/static/{self.NAME}
        REACT_APP_NAME={self.NAME}
        REACT_APP_ENDPOINT={self.ENDPOINT}
        REACT_APP_IS_INDEX={self.IS_INDEX}
        REACT_APP_API={api}
        REACT_APP_PWA={pwa}
        BUILD_PATH={settings.BASE_DIR + '/static/' + self.NAME}
        '''.replace('    ', '')

    def _path(self, file_name):
        '''
        Use this function to get the raw string containing the complete path
        for the file you would like to serve.
        '''
        return settings.BASE_DIR + f"/static/{self.NAME}/{file_name}"

    def is_native():
        '''
        Lets the Overlord know that this is not a React-Native based Client
        and it is a default React Web App based client

        :return: False
        '''
        return False

    def app(self, req, *args, **kwargs):
        '''
        Renders and returns the app index file

        :return: text/html http response
        '''
        return render(
            req,
            self._path('index'),
            content_type='text/html'
        )

    def robots(self, req, *args, **kwargs):
        return render(req, self._path('robots.txt'), content_type='text/plain')

    def manifest(self, req, *args, **kwargs):
        return render(req, self._path('manifest.json'), content_type='application/json')

    def assets(self, req, *args, **kwargs):
        return render(req, self._path('asset-manifest.json'), content_type='application/json')

    def service_worker(self, req, *args, **kwargs):
        return render(req, self._path('service-worker.js'), content_type='application/x-javascript')

    def service_worker_map(self, req, *args, **kwargs):
        return render(req, self._path('service-worker.js.map'), content_type='application/x-javascript')


class NativeClient():
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

    # Client.ENVIRONMENT [ local, staging, production... ]
    ENV = ''

    # Client.NAME and directory name for this client source files should be identical
    NAME = ''

    # Client.PORT by default will be automatically determined if PORT is None.
    # otherwise you can specify a port number as a string.
    PORT = RPU()

    # Client.ENDPOINT controls which `base url` will host your application
    # By default, only the INDEX client can connect to the root (http..com/) url
    # Also, all paths beginning with this ENDPOINT will instead be forwarded to
    # this application - this is why we give the INDEX setting special treatment.
    ENDPOINT = NAME if not NAME == settings.INDEX else ''
    IS_INDEX = str(ENDPOINT == '').lower()

    # Client.API is a string representing which endpoint to connect to when making API
    # requests. By default, `http../api` will be used if API is set to `None`
    API = ''

    # Client.PWA is a boolean which indicates whether or not to enable service workers
    PWA = False

    def __init__(self):
        # User setup dependent options
        if self.ENDPOINT == '':
            self.ENDPOINT = self.NAME if not self.NAME == settings.INDEX else ''
        self.IS_INDEX = str(self.ENDPOINT == '').lower()
        # Generate local environment file
        with open(self.ENV, '+w') as env:
            env.write(self._env())
        # Build the url structure for django
        self.URL = self._url()

    def _url(self):
        # Client.URL is a re_path pointing towards to the app index file
        return re_path(r"^(?!static)^(?!assets)^(?!api).*$", self.app, name=f"{self.NAME} App")

    def _env(self):
        '''
        Generate Client Environment Configuration

        Creates the .env file for this client on this environment which
        automatically adjusts between local development, staging or production
        '''
        port = self.PORT if self.PORT is not None else RPU()
        api = self.API if self.API is not None else 'api'
        pwa = 'true' if self.PWA else 'false'

        return f'''# .env
        #   automatically generated file
        #   do not edit or delete
        PORT={port}
        PUBLIC_URL=/static/{self.NAME}
        REACT_APP_NAME={self.NAME}
        REACT_APP_ENDPOINT={self.ENDPOINT}
        REACT_APP_IS_INDEX={self.IS_INDEX}
        REACT_APP_API={api}
        REACT_APP_PWA={pwa}
        '''.replace('    ', '')

    def _path(self, file_name):
        '''
        Use this function to get the raw string containing the complete path
        for the file you would like to serve.
        '''
        return settings.BASE_DIR + f"/static/{self.NAME}/{file_name}"

    def is_native():
        '''
        Lets the Overlord know that this is a React-Native based Client
        as opposed to a regular default React Web App.

        :return: True
        '''
        return True

    def app(self, req, *args, **kwargs):
        '''
        Renders and returns the app index file

        :return: text/html http response
        '''
        return render(
            req,
            self._path('index'),
            content_type='text/html'
        )

    def robots(self, req, *args, **kwargs):
        return render(req, self._path('robots.txt'), content_type='text/plain')

    def manifest(self, req, *args, **kwargs):
        return render(req, self._path('manifest.json'), content_type='application/json')

    def assets(self, req, *args, **kwargs):
        return render(req, self._path('asset-manifest.json'), content_type='application/json')

    def service_worker(self, req, *args, **kwargs):
        return render(req, self._path('service-worker.js'), content_type='application/x-javascript')

    def service_worker_map(self, req, *args, **kwargs):
        return render(req, self._path('service-worker.js.map'), content_type='application/x-javascript')
