#
# SET DEFAULT SITE STYLE FOR ALL CLIENTS
#
default = {
    'html': {
        'font-family': 'Helvetica',
        'font-weight': 'normal',
        'overflow-x': 'hidden',
        'min-height': '100%',
        'min-width': '100%',
        'color': 'white',
        'background-color': '#11151A'
    },
    '::selection': {
        'background': '#b53e31'
    },
    '::-moz-selection': {
        'background': '#b53e31'
    },
    '::-webkit-scrollbar': {
        'width': '6px',
        'background-color': '#201c29'
    },
    '::-webkit-scrollbar-thumb': {
        'background-color': '#666',
    },
    'svg': {
        'fill': '#fe8605',
        'min-width': '100%',
        'min-height': '100%'
    },
    'svg:active': {
        'fill': 'white'
    },
    'img': {
        'margin': '16px 20% 16px 20%',
        'width': '60%',
        'box-shadow': '1px 1px 15px rgba(1,1,1,1)'
    },
    'h1,h2,h3,h4,h5,h6': {
        'color': 'white',
        'margin': '.1rem 0 0 0'
    },
    'p': {
        'text-align': 'left',
        'margin': '0 0 0 0',
        'color': 'white'
    },
    'input': {
        'width': '90%',
        'margin': '0 16px 0 16px'
    },
    'button': {
        'background-color': 'rgba(99, 99, 99, 0.1)'
    },
    '.button': {
        'width': '100%',
        'color': 'white'
    },
    '.tab': {
        'color': 'white',
        'font-family': 'Caesar Dressing',
        'font-size': '2rem',
        'width': '300px',
        'height': '64px',
        'margin': '32px 16px 32px 16px',
        'border-radius': '0',
        'background-color': 'rgba(1, 1, 1, 0)'
    },
    '.tab:hover': {
        'background-color': 'rgba(217, 117, 11, 0.5)'
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
        'top': '95px',
        'overflow-x': 'hidden'
    },
    '.content': {
        'top': '46px',
        'border': '0',
        'left': '0px',
        'width': '100%',
        'position': 'fixed',
        'background-color': 'rgba(55,55,55,1)'
    },
    '.menu': {
        'width': '100%',
        'max-height': '310px',
        'overflow-y': 'auto',
        'overflow-x': 'hidden',
        'text-align': 'center',
        'display': 'none',
        'scrollbar-width': '1px',
        'scrollbar-color': '#666 #201c29'
    },
    '.app-bar': {
        'box-shadow': '1px 1px 5px rgba(1,1,1,1)',
        'min-height': '36px',
        'z-index': '99',
        'position': 'fixed',
        'left': '0px',
        'bottom': '0px'
    },
    '.app-bar-option:hover': {
        'background-color': '#fe8605'
    },
    '.youtube-video': {
        'width': '100%',
        'height': '100%',
        'max-width': '800px',
        'min-width': '300px',
        'min-height': '480px',
        'margin': '32px 0 32px 0',
        'background-color': 'black'
    },
    'twitter-follow-button': {
        'margin': '0 0 0 0'
    },
    'instagram-media': {
        'width': '480px',
        'height': '640px'
    },
    '.site-header': {
        'margin': '32px 0 64px 0'
    }
}

#
# DEFAULT MODE FOR DESKTOPS
#
landscape = {
    '.app-bar': {
        'background-color': 'rgba(10, 10, 10, 0.9)',
        'margin': '0 0 8px 8px',
        'min-width': '210px',
        'width': '20%'
    },
    '.content': {
        'height': 'calc(100% - 48px)',
    },
    '.youtube-div': {
        'padding': '10% 20% 10% 20%',
        'box-shadow': '1px 1px 15px rgba(1,1,1,1)'
    },
    '.youtube-desc': {
        'margin': '0 20% 0 20%'
    },
    '.site-header': {
        'display': 'flex',
        'justify-content': 'center'
    },
    '.site-header-logo': {
        'width': '30%',
        'margin-left': '-10%',
        'margin-right': '15%'
    }
}

#
# DEFAULT MODE FOR MOBILE
#
portrait = {
    '.app-bar': {
        'background-color': 'rgba(10, 10, 10, 1)',
        'margin': '0 0 0 0',
        'width': '100%'
    },
    '.content': {
        'height': 'calc(100% - 112px)',
    },
    '.youtube-div': {
        'padding': '10% 5% 10% 5%'
    },
    '.youtube-desc': {
        'margin': '0 20% 0 20%'
    },
    '.site-header': {
        'display': 'block',
        'justify-content': 'center'
    },
    '.site-header-logo': {
        'width': '100%',
        'margin-left': '0'
    }
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

