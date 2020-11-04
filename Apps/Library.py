from Overlord.Canopy.Core import Document
from Overlord.Canopy.Elements import element
from Overlord.Canopy.Image import svg

# Page Root
App = Document()
App.import_css('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap')
App.import_css('https://fonts.googleapis.com/css2?family=Spartan:wght@700&display=swap')
App.set_font("Roboto")


def library_category(icon=str(), label=str()):
    return element(
        Class='library-category',
        Items=icon + "<h6>" + label + "</h6>"
    )


def library_section(ID):
    return element(
        ID='library_section_' + ID,
        Class='library-section',
        Items='''
        <h4 style='text-align:left;'>{label}</h4>
        <hr>
        <div style='min-height:250px;display:flex;flex-wrap:wrap;padding:15px 15px 5px 15px;'>
            <div>
                <div style='
                    border:1px solid grey;
                    width:200px;
                    height:200px;
                    background-image:url(/Image/budgetGraph.png);
                    '>
                </div>
                <h3 style='margin-top:6px;'>Budget</h3>
            </div>
        </div>
        '''.format(label=ID)
    )


# Page Elements
App.add_elements(
    element(
        Class='library-category-section',
        Items=[
            library_category(icon=svg('spanner'), label='Engineering'),
            library_category(icon=svg('gamepad'), label='Entertainment'),
            library_category(icon=svg('badge'), label='Enterprise'),
            library_category(icon=svg('education'), label='Education')
        ]
    ),
    library_section('Favourites'),
    library_section('Reccomended')
)

# Page Render
App = App.render()
