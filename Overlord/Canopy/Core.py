from . import Themes, Templates
from ..Bionic.Basics import open_file, root

pages = []
jsenv = {
    'c': '0',
    '0': """ """.replace('\n', '')
}


def script(function, parameters=''):
    if function not in jsenv['0'] and function not in jsenv[jsenv['c']]:
        jsenv[jsenv['c']] += \
            open_file(root + '/Static/JS', function + '.js').\
                replace('\n', ' ') + '\n        '
    if not ',' in parameters:
        return function + """(`""" + str(parameters) + """`);"""
    return function + """(""" + str(parameters) + """);"""


def var(variable, value):
    if isinstance(value, str):
        return variable + """ = `""" + value +  """`;"""


'''
    UI mode enables behaviour to reset 
    toggled content back to it's 'x'
    state if another UI element is 
    selected.
'''
def toggleContent(ID, x, y, display='', UI_MODE=False):
    if UI_MODE:
        return script(
            '''toggleUI''', 
            '''`''' + ID + '''`, 
            `''' + x + '''`, 
            `''' + y + '''`
            `''' + display + '''`
            '''
        )
    return script(
            '''toggleInner''', 
            '''`''' + ID + '''`, 
            `''' + x + '''`, 
            `''' + y + '''`
            '''
        )


class Document:

    def __init__(self):
        global jsenv
        self.jsenv = str(len(jsenv))
        jsenv['c'] = self.jsenv
        jsenv[self.jsenv] = str()
        self.styles = {
            'default': Themes.default,
            'landscape': Themes.landscape, 
            'portrait': Themes.portrait
        }
        self.elements = Templates.default
        self.footer = list()

    def add_elements(self, elements=list()):
        for element in elements:
            if isinstance(str, element):
                self.elements.append(str(element))

    def render(self):
        return """<!DOCTYPE html>
<html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script type="text/javascript">
        """ + jsenv['0'] + """
        """ + jsenv[self.jsenv] + """ 
    </script>
    <style> 
    """ + \
    Themes.style(
        self.styles['default'],
    ) + """
    """ + Themes.style(
        self.styles['landscape'], 
        rules={'orientation': 'landscape'}
    ) + \
    Themes.style(
        self.styles['portrait'],    
        rules={'orientation': 'portrait'}
    ) + """ 
    </style>
    </head>
    <div id='site.body' class='site-body'>
        """ + ''.join(self.elements) + """ 
    </div>
</html>
"""

