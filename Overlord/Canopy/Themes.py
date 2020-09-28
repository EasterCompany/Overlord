#
# SET DEFAULT SITE STYLE FOR ALL CLIENTS
#
default = {
    'html': {
        'font-family': 'helvetica',
        'font-weight': 'normal',
        'color': 'white',
        'text-align': 'center',
        'scrollbar-color': '#666 #201c29',
        'overflow-x': 'hidden',
        'min-height': '100%',
        'min-width': '100%',
        'background-color': 'rgba(55, 55, 55, 1)'
    },
    '::selection': {
        'background': '#b53e31'
    },
    '::-moz-selection': {
        'background': '#b53e31'
    },
    'svg': {
        'fill': '#fe8605',
        'min-width': '100%',
        'min-height': '100%'
    },
    'svg:active': {
        'fill': 'white'
    },
    'h1,h2,h3,h4,h5,h6': {
        'margin': '.1rem 0 0 0'
    },
    'p': {
        'text-align': 'left',
        'margin': '0 0 0 0'
    },
    'hr': {
        'margin': '1% 1% 1% 1%',
    },
    '.button': {
        'width': '100%',
        'color': 'white',
        'padding': '2px 0 2px 0',
        'background-color': 'rgba(99, 99, 99, 0.5)'
    },
    '.button:hover': {
        'background-color': 'rgba(255, 99, 71, 0.5)',
        'border-color': 'rgba(255, 99, 71, 1)',
    },
    '.nav-bar': {
        'background-color': 'rgba(10, 10, 10, 0.5)',
        'box-shadow': '1px 1px 5px rgba(1,1,1,1)',
        'width': '100%',
        'display': 'flex',
        'overflow': 'hidden',
        'z-index': '99',
        'position': 'fixed',
        'left': '0px',
        'top': '0px'
    },
    '.site-body': {
        'text-align': 'center',
        'z-index': '-1',
        'color': 'black',
        'top': '95px',
        'overflow-x': 'hidden',
        'margin': '95px 0 95px 0',
    },
    '.content': {
        'top': '48px',
        'left': '0px',
        'position': 'fixed',
        'height': '100%',
        'width': '100%',
        'background-color': 'rgba(55, 55, 55, 1)'
    },
    '.menu': {
        'width': '250px',
        'text-align': 'center',
        'display': 'none'
    },
    '.app-bar': {
        'background-color': 'rgba(10, 10, 10, 0.7)',
        'box-shadow': '1px 1px 5px rgba(1,1,1,1)',
        'min-height': '64px',
        'z-index': '99',
        'position': 'fixed',
        'left': '0px',
        'bottom': '0px'
    },
    '.app-bar-option:hover': {
        'background-color': '#fe8605'
    }
}

#
# DEFAULT MODE FOR DESKTOP CLIENTS
#
landscape = {
    '.app-bar': {
        'padding': '8px 8px 8px 8px',
        'margin': '0 0 8px 8px',
        'width': '250px',
    },
    'body': {
        'padding': '2% 2% 0 2%',
        'height': 'calc(98% - 48px)',
        'width': '90%'
    },
}

#
# DEFAULT MODE FOR MOBILE CLIENTS
#
portrait = {
    '.app-bar': {
        'padding': '8px calc(50% - 132px) 8px calc(50% - 132px)',
        'margin': '0 0 0 0',
        'width': '100%',
    },
    'body': {
        'padding': '2% 1% 0 1%',
        'height': 'calc(98% - 48px)',
        'width': '98%',
    },
}


#
# CONVERT STYLE DICTIONARY TO CSS 
#
def style(style_dict, rules=None):
    css = """"""
    for style in style_dict:
        css += style + """{"""
        for atr in style_dict[style]:
            css += atr + """:""" + style_dict[style][atr] + """;"""
        css += """}"""
    if rules is not None and isinstance(rules, dict):
        r = "@media "
        for index, rule in enumerate(rules):
            if index > 0: r += " and "
            r += "(" + rule + ":" + rules[rule] + ")"
            return r + """{
    """ + css + """
    }"""
    return css

