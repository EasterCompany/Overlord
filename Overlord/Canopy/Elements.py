

def html(
    _tag=str(), _content=str(), _id=str(), _src=str(), 
    _class=str(), _style=str(), _onclick=str()
    ):
    return """<""" + _tag + _id + _src + _style + _class + _onclick + """> 
        """ + _content + """ </""" + _tag + """>"""


def element(
    Tag='div', Items=None, ID=str(), Source=str(),
    Class=str(), OnClick=str(), Style=str()
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
    # render
    return html(
        _tag=Tag,
        _id=ID,
        _src=Source,
        _style=Style,
        _class=Class,
        _content=Items,
        _onclick=OnClick
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


def button(Icon=str(), OnClick=str(), ID='button', Border=False, Text=str()): 
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
        Class=ID,
        OnClick=OnClick
    )
    if Border:
        r += "<hr/>"
    return r


def navbar(elements=list()):
    return element(
        Class="nav-bar",
        Items=elements
    )


def appbar(elements=list()):
    return element(
        Class="app-bar",
        Items=elements
    )


def content(elements=list(), source=str()):
    if not source == '':
        return element(
            Tag='iframe',
            ID='content',
            Class='content',
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


e = element
