

def html(
    _tag=str(), _content=str(), _id=str(), _src=str(), _class=str(),
    _style=str(), _onclick=str(), _onload=str(), _href=str()
    ):
    return """<""" + _tag + _id + _src + _style + _class + _onclick + _onload + _href + """>
        """ + _content + """ </""" + _tag + """>"""


def element(
    Tag='div', Items=None, ID=str(), Source=str(),
    Class=str(), OnClick=str(), OnLoad=str(), Style=str(), Href=str()
    ):
    # id
    if ID is not None and isinstance(ID, str) and not ID == '':
        ID = " id='" + ID + "'"
    elif not isinstance(ID, str):
        print("""an elements 'ID' parameter must be a string""", ID), exit(code=100)
    else:
        ID = ""
    # class
    if Class is not None and isinstance(Class, str) and not Class == '':
        Class = " class='" + Class + "'"
    elif not isinstance(Class, str):
        print("""an elements 'Class' parameter must be a string""", Class), exit(code=101)
    else:
        Class = ""
    # onclick
    if OnClick is not None and isinstance(OnClick, str) and not OnClick == '':
        OnClick = " onclick='" + OnClick + "'"
    elif not isinstance(OnClick, str):
        print("""an elements 'OnClick' parameter must be a string""", OnClick), exit(code=102)
    else:
        OnClick = ""
    # onload
    if OnLoad is not None and isinstance(OnLoad, str) and not OnLoad == '':
        OnLoad = " onload='" + OnLoad + "'"
    elif not isinstance(OnLoad, str):
        print("""an elements 'OnLoad' parameter must be a string""", OnLoad), exit(code=106)
    else:
        OnLoad = ""
    # items
    if Items is not None and isinstance(Items, list) and not len(Items) == 0:
        Items = " ".join(Items)
    elif Items is not None and not isinstance(Items, list):
        Items = str(Items)
    else:
        Items = ""
    # style
    if Style is not None and isinstance(Style, str) and not Style == '':
        Style = " style='" + Style + "'"
    elif not isinstance(Style, str):
        print("""an elements 'Style' parameter must be a string""", exit(code=103))
    else:
        Style = ""
    # source
    if Source is not None and isinstance(Source, str) and not Source == '':
        Source = " src='" + Source + "'"
    elif not isinstance(Source, str):
        print("""an elements 'Source' parameter must be a string""", exit(code=104))
    else:
        Source = ""
    # class
    if Href is not None and isinstance(Href, str) and not Href == '':
        Href = " href='" + Href + "'"
    elif not isinstance(Href, str):
        print("""an elements 'Href' parameter must be a string""", Href), exit(code=101)
    else:
        Href = ""
    # render
    return html(
        _tag=Tag,
        _id=ID,
        _src=Source,
        _style=Style,
        _class=Class,
        _content=Items,
        _onclick=OnClick,
        _onload=OnLoad,
        _href=Href
    )


def flex(*args):
    return element(Style='display:flex;', Items=''.join(args))


def block(*args):
    return element(Style='display:block;', Items=''.join(args))


def key_input(Class='search-bar'):
    return element(
        Tag="input",
        ID=Class,
        Class=Class,
    )


def button(Icon=str(), OnClick=str(), ID='button', Class='button', Border=False, Text=str()):
    _tag = 'div'
    _items = Icon
    if Text is not str():
        _items += element(
            Tag="h3",
            Items=[Text, ]
        )
    r = element(
        Tag=_tag,
        Items=_items,
        ID=ID,
        Class=Class,
        OnClick=OnClick
    )
    if Border:
        r += "<hr/>"
    return r


def navbar(elements=list()):
    return element(
        Class="navbar",
        Items=elements
    )


def appbar(elements=list()):
    return element(
        ID="app_bar",
        Class="app-bar",
        Items=elements
    )


def content(elements=list(), source=str()):
    if not source == '':
        return element(
            Tag='iframe',
            ID='content',
            Class='content',
            OnLoad='__update__();',
            Items=elements,
            Source=source
        )
    return element(
        ID='content',
        Class='content',
        Items=elements
    )


def menu(ID="menu", Class="menu", elements=list()):
    return element(
        ID=ID,
        Class=Class,
        Items=elements
    )


def dropmenu(elements=list(), ID='dropmenu'):
    return menu(
        ID=ID,
        elements=elements
    )


def form(*args):
    return """
    <div style='
        display:flex;
        justify-content:space-around;
        width:100%;
        max-height:90%;
        margin:5% 0 5% 0;
    '>
        <form onsubmit='return false;'
            style='
                text-align:left;
                padding:24px 24px 24px 24px;
                min-width:245px;
                width:20%;
                background-color:#202029;
                box-shadow: 0 0 3px white;
                border:1px solid grey;
                border-radius:3px;
            '>""" + str(*args) + """
        </form>
    </div>
    """


def shader():
    return element(
        Style="""
            margin:32px 0 16px 0;
            box-shadow: 0px -8px 8px rgba(25, 25, 25, 1);
        """,
        Items='&nbsp;'
    )


def story(align='left', header='', text='', image=''):

    image = """<div style='
            min-width:300px;
            min-height:300px;
            max-width:300px;
            max-height:300px;
            background-size:100% auto;
            background-image:url({image});
            background-repeat:no-repeat;
        '>""".format(image=image) + \
            "&nbsp;" + \
        "</div>"

    text = "<div style='margin:32px 32px 32px 32px;min-width:300px;max-width:600px;'>" + \
            "<h1>" + header + "</h1>" + \
            text + \
        "</div>"

    if align == 'left':
        this = image + text
    else:
        this = text + image

    return element(
        Items=[
            """<div style='
                display:flex;
                flex-wrap:wrap;
                justify-content:center;
                min-width:300px;
                margin:32px auto;'>
            """,
                this,
            "</div>"
        ]
    )


e = element
