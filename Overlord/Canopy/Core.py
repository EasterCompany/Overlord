from . import Themes, Templates
from ..Bionic.Basics import open_file, root, py_args, \
    syspath, mkdir

pages = []
jsenv = {
    'c': '0',
    '0': """ """.replace('\n', '')
}


def script(function, parameters=''):
    if function not in jsenv['0'] and function not in jsenv[jsenv['c']] and \
        syspath.exists(root + '/Static/JS/' + function + '.js'):
        jsenv[jsenv['c']] += \
            open_file(root + '/Static/JS', function + '.js').\
                replace('\n', ' ') + '\n        '
    if not ',' in parameters:
        return function + """(`""" + str(parameters) + """`);"""
    return function + """(""" + str(parameters) + """);"""


def var(variable, value):
    if isinstance(value, str):
        return variable + """=`""" + value +  """`;"""


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

    def __init__(self, template=list()):
        global jsenv
        self.jsenv = str(len(jsenv))
        jsenv['c'] = self.jsenv
        jsenv[self.jsenv] = str()
        self.styles = {
            'default': Themes.default,
            'landscape': Themes.landscape, 
            'portrait': Themes.portrait
        }
        self.elements = template
        self.css_imports = []

    def import_css(self, href):
        return self.css_imports.append(href)

    def set_font(self, family):
        self.styles['default']['html']['font-family'] = family

    def add_elements(self, elements=list()):
        for element in elements:
            self.elements.append(str(element))

    def minifyBuild(self, target):
        _build = target.replace('\n', ' ')
        while '  ' in _build:
            _build = _build.replace('  ', ' ')
        return _build

    def render(self):
        style = Themes.style(
        self.styles['default'],
        ) + """
        """ + Themes.style(
            self.styles['landscape'], 
            rules={'orientation': 'landscape'}
        ) + \
        Themes.style(
            self.styles['portrait'],    
            rules={'orientation': 'portrait'}
        )
        import_styles = ""
        for css_import in self.css_imports:
            import_styles += """
                <link rel="stylesheet" href="{new_import}">
            """.format(new_import=css_import)
        render = """<!DOCTYPE html>
<html>
    <head>
    <title> Easter Company </title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """ + import_styles + """
    <script type="text/javascript">
        """ + jsenv['0'] + """
        """ + jsenv[self.jsenv] + """ 
    </script>
    <style> 
    """ + style + """ 
    </style>
    </head>
    <div id='site.body' class='site-body'>
        """ + ''.join(self.elements) + """ 
    </div>
</html>
"""
        if '-t' in py_args:
            return render
        return self.minifyBuild(render)

