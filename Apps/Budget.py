# Page Imports
from Overlord.Canopy.Core import Document, script
from Overlord.Canopy.Elements import element

# Page Root
App = Document()
App.import_css('https://fonts.googleapis.com/css2?family=Spartan:wght@700&display=swap')
App.set_font('Spartan')


# Page Objects
def my_balance():
    return element(
        Style="display:block;width:220px;",
        Items=[
            element(
                Tag="h5",
                Style="color:peru;text-align:left;margin:8px 1% 8px 1%;",
                Items="MY BALANCE"
            ),
            element(
                Tag="h1",
                Style="color:orange;text-align:left;margin:8px 1% 8px 1%;",
                Items="£420.69"
            ),
            element(
                Tag="h5",
                Style="color:peru;text-align:left;margin:8px 1% 8px 1%;",
                Items="saving: + 420.69 pm"
            )
        ]
    )


def my_change():
    return element(
        Style="display:block;width:180px;",
        Items=[
            element(
                Tag="h5",
                Style="color:peru;text-align:left;margin:8px 1% 8px 1%;",
                Items="CHANGE P/M"
            ),
            element(
                Tag="h1",
                Style="color:green;text-align:left;margin:8px 1% 8px 1%;",
                Items="+99%"
            ),
            element(
                Tag="h5",
                Style="color:peru;text-align:left;margin:8px 1% 8px 1%;",
                Items="last: -69%"
            )
        ]
    )


def my_chart():
    return element(
        ID="budgetChart",
        Tag="canvas",
        Style="""
            margin:32px 0 16px 0;
            width:300px;
            height:300px;
        """
    )


def my_status():
    return element(
        Style="""
            overflow:hidden;
            display:flex;
            margin:6px 0 0 0;
            justify-content:center;
            border-left:6px solid peru;
            background-color:rgba(25,25,25,.5);",
            """,
        Items=[
            my_balance(),
            my_change()
        ]
    )


# Page Content
App.add_elements(
    my_status(),
    my_chart(),
    script(
        function='chart',
        parameters='''
            `budgetChart`,
            {
                "saving": 15,
                "utility": 10,
                "housing": 25,
                "food & drink": 20,
                "entertainment": 30 
            },
            0.5
        ''',
        addon=True
    )
)

# Page Render
App = App.render()
