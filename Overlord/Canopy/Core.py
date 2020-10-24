from . import Themes
from ..Bionic.Basics import open_file, root, py_args, \
    syspath

pages = []
jsenv = {
    'c': '0',
    '0': ""
}


def script(function, parameters='', addon=False):
    if function not in jsenv['0'] and function not in jsenv[jsenv['c']] and \
        syspath.exists(root + '/Static/JS/' + function + '.js'):
        jsenv[jsenv['c']] += \
            open_file(root + '/Static/JS', function + '.js').\
                replace('\n', ' ')
        while '  ' in jsenv[jsenv['c']]:
            jsenv[jsenv['c']] = jsenv[jsenv['c']].replace('  ', ' ')
    if not ',' in parameters:
        r = function + """(`""" + str(parameters) + """`);"""
    else:
        r = function + """(""" + str(parameters) + """);"""
    if addon:
        return "<script>" + r + "</script>"
    return r


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

    def __init__(self, template=None, styles=None):
        global jsenv
        self.jsenv = str(len(jsenv))
        jsenv['c'] = self.jsenv
        jsenv[self.jsenv] = str()
        self.styles = {
            'default': Themes.default,
            'landscape': Themes.landscape, 
            'portrait': Themes.portrait
        }
        if template is None:
            template = []
        if styles is None:
            styles = []
        self.elements = template
        self.css_imports = styles
        self.set_font('open sans')

    def import_css(self, href):
        return self.css_imports.append(href)

    def set_font(self, family):
        self.styles['default']['html']['font-family'] = family

    def add_elements(self, *args):
        for element in args:
            self.elements.append(str(element))

    @staticmethod
    def minifyBuild(target):
        _build = target.replace('\n', ' ')
        while '  ' in _build:
            _build = _build.replace('  ', ' ')
        return _build

    # Add this when the appropriate time stamp library is available
    # <meta property="og:updated_time" content="2020-04-01T14:20:02+01:00">
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
    <meta name="description" content="Parent Company which focuses around building Engineering, Education, Enterprise & Entertainment Applications."/>
    <meta name="robots" content="index,follow,max-snippet:-1,max-video-preview:-1,max-image-preview:large"/>
    <link rel="canonical" href="https://www.easter.company/"/>
    <meta property="og:locale" content="en_GB">
    <meta property="og:type" content="article">
    <meta property="og:title" content="Easter Company">
    <meta property="og:description" content="Parent Company which focuses around building Engineering, Education, Enterprise & Entertainment Applications.">
    <meta property="og:url" content="https://www.easter.company/">
    <meta property="og:site_name" content="Easter Company">
    <meta property="og:image" content="https://scontent-lht6-1.xx.fbcdn.net/v/t1.0-9/120997568_790377715071585_9083588456177368086_o.png?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=FTk8Cvw9mkQAX-7uXMZ&_nc_ht=scontent-lht6-1.xx&oh=b92f0ba784e60e9eb8845cc3e53c786f&oe=5FB6D8D1">
    <meta property="og:image:secure_url" content="https://scontent-lht6-1.xx.fbcdn.net/v/t1.0-9/120997568_790377715071585_9083588456177368086_o.png?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=FTk8Cvw9mkQAX-7uXMZ&_nc_ht=scontent-lht6-1.xx&oh=b92f0ba784e60e9eb8845cc3e53c786f&oe=5FB6D8D1">
    <meta property="og:image:width" content="1920">
    <meta property="og:image:height" content="1080">
    <meta property="og:image:alt" content="Easter Company">
    <meta property="og:image:type" content="image/png">
    <meta property="og:updated_time" content="2020-10-10T20:20:20+01:00">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Easter Company">
    <meta name="twitter:description" content="Parent Company which focuses around building Engineering, Education, Enterprise & Entertainment Applications.">
    <meta name="twitter:image" content="https://scontent-lht6-1.xx.fbcdn.net/v/t1.0-9/120997568_790377715071585_9083588456177368086_o.png?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=FTk8Cvw9mkQAX-7uXMZ&_nc_ht=scontent-lht6-1.xx&oh=b92f0ba784e60e9eb8845cc3e53c786f&oe=5FB6D8D1">
    <link rel='stylesheet' id='opensans-css'  href='https://fonts.googleapis.com/css?family=Open+Sans%7COswald%3A700&#038;ver=5.3.4#038;ver=5.2.2' type='text/css' media='all' />
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

