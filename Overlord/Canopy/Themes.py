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
        'background-color': '#202029',
        'scroll-behavior': 'smooth'
    },
    '::selection': {
        'background': '#b53e31'
    },
    '::-moz-selection': {
        'background': '#b53e31'
    },
    '::-webkit-scrollbar': {
        'width': '6px',
        'height': '6px',
        'background-color': '#201c29'
    },
    '::-webkit-scrollbar-thumb': {
        'background-color': '#666'
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
        'font-family': 'Spartan',
        'margin': '.1rem 0 .1rem 0'
    },
    'p': {
        'text-align': 'left',
        'margin': '0 0 0 0',
        'color': 'white'
    },
    'a': {
        'color': 'peru'
    },
    'input,select': {
        'width': '95%',
        'height': '32px',
        'margin': '0 1% 0 1%',
        'color': 'rgba(200,200,200,1)',
        'background-color': 'rgba(25,25,25,.5)',
        'border-radius': '6px'
    },
    'button': {
        'background-color': 'rgba(99, 99, 99, 0.1)'
    },
    '.button': {
        'width': '100%',
        'padding': '2px 2px 2px 2px',
        'min-height': '32px',
        'color': 'white',
        'cursor': 'pointer'
    },
    '.tab': {
        'color': 'white',
        'cursor': 'pointer',
        'font-size': '2rem',
        'width': '300px',
        'height': '64px',
        'margin': '32px 16px 32px 16px',
        'border-radius': '0',
        'background-color': 'rgba(1, 1, 1, 0.1)'
    },
    '.tab:hover': {
        'background-color': 'rgba(217, 117, 17, 0.17)'
    },
    '.button:hover': {
        'background-color': 'rgba(255, 99, 71, 0.5)',
        'border-color': 'rgba(255, 99, 71, 1)',
    },
    '.navbar': {
        'background-color': 'rgba(35, 35, 35, 1)',
        'box-shadow': '1px 1px 5px rgba(1,1,1,1)',
        'padding': '3px 0 3px 0',
        'width': '100%',
        'max-height': '32px',
        'display': 'flex',
        'overflow': 'hidden',
        'z-index': '99',
        'position': 'fixed',
        'left': '0px',
        'top': '0px'
    },
    '.shader': {
        'background-color': 'rgba(0,0,0,0.3)'
    },
    '.site-body': {
        'text-align': 'center',
        'z-index': '-1',
        'top': '95px',
        'overflow-x': 'hidden'
    },
    '.content': {
        'top': '40px',
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
        'font-family': 'Roboto',
        'background-color': 'rgba(25, 25, 25, 1)',
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
    '.youtube-div': {
        'box-shadow': '1px 1px 15px rgba(1,1,1,1)'
    },
    '.youtube-video': {
        'width': '100%',
        'height': '100%',
        'max-width': '800px',
        'min-width': '300px',
        'min-height': '480px',
        'margin': '2% 0 2% 0',
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
        'max-width': '600px',
        'margin': '32px auto',
        'justify-content': 'center'
    },
    '.site-header-logo': {
        'margin': '0 auto'
    },
    '.site-header-quote': {
        'font-family': 'Roboto'
    },
    '.library-category-section': {
        'overflow-x': 'scroll',
        'display': 'flex',
        'width': '100%',
        'max-height': '80px',
        'padding-bottom': '6px'
    },
    '.library-category': {
        'cursor': 'pointer',
        'width': '100%',
        'min-width': '96px',
        'margin': '0 auto',
        'padding': '4px 4px 20px 4px',
        'font-family': 'Roboto'
    },
    '.library-category:hover': {
        'background-color': 'rgba(217, 117, 17, 0.17)'
    },
    '.library-category:active': {
        'background-color': 'peru'
    },
    '.library-section': {
        'margin': '0 auto',
        'padding': '16px 8px 16px 8px',
        'width': '96%'
    },
    '.grid-row': {
        'border-bottom': '1px solid grey',
        'padding': '3px 3px 3px 3px',
        'display': 'flex'
    },
    '.grid-cell': {
        'border-right':'1px solid grey',
        'width': '25%',
        'padding-top': '6px',
        'overflow': 'hidden',
        'font-size': '.8rem'
    },
    '.grid-row-delete': {
        'width': '20px',
        'height': '20px',
        'padding': '4px 4px 4px 4px'
    },
    '.app-library-image': {
        'border-radius': '40%',
        'min-width': '100px',
        'min-height': '100px',
        'background-size': '100%',
        'background-repeat': 'no-repeat'
    },
    '.app-library-app': {
        'width': '100px',
        'height': '130px'
    },
    '.app-library-app:hover': {
        'cursor': 'pointer',
        'background-color': 'rgba(25,25,25,.5)'
    }
}

#
# DEFAULT MODE FOR DESKTOPS
#
landscape = {
    '.app-bar': {
        'margin': '0 0 8px 8px',
        'min-width': '210px',
        'width': '15%'
    },
    '.content': {
        'height': 'calc(100% - 40px)'
    },
    '.youtube-div': {
        'padding': '10% 20% 10% 20%',
    },
    '.youtube-desc': {
        'margin': '0 20% 0 20%'
    }
}

#
# DEFAULT MODE FOR MOBILE
#
portrait = {
    '.app-bar': {
        'margin': '0 0 0 0',
        'width': '100%'
    },
    '.content': {
        'height': 'calc(100% - 96px)',
    },
    '.youtube-div': {
        'padding': '10% 5% 10% 5%'
    },
    '.youtube-desc': {
        'margin': '0 20% 0 20%'
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

