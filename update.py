from Overlord.Bionic.Update import *


class application:
    cert = approve_certificate(
            fetch_source()
        )
    
    def __init__(self):
        self.source = dict()
        if self.cert == 1:
            self.source['ver'] = '+'
        elif self.cert == 0:
            self.source['ver'] = '='
        elif self.cert == -1:
            self.source['ver'] = '?'

