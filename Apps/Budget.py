# Page Imports
from Overlord.Canopy.Core import Document, script
from Overlord.Canopy.Elements import element
from Overlord.Canopy.Image import svg

# Page Root
App = Document()
App.import_css('https://fonts.googleapis.com/css2?family=Spartan:wght@700&display=swap')
App.set_font('Spartan')


# Page Objects
def my_balance():
    return element(
        Style="display:block;width:190px;",
        Items=[
            element(
                Tag="h5",
                Style="color:peru;text-align:left;margin:8px 1% 8px 1%;",
                Items="MY BALANCE"
            ),
            element(
                Tag="h1",
                Style="color:orange;text-align:left;margin:8px 1% 8px 1%;",
                Items="£0.00"
            ),
            element(
                Tag="h5",
                Style="color:peru;text-align:left;margin:8px 1% 8px 1%;",
                Items="saving: 0.00 pm"
            )
        ]
    )


def my_change():
    return element(
        Style="display:block;width:106px;",
        Items=[
            element(
                Tag="h5",
                Style="color:peru;text-align:left;margin:8px 1% 8px 1%;",
                Items="AVG CHANGE"
            ),
            element(
                Tag="h1",
                Style="color:peru;text-align:left;margin:8px 1% 8px 1%;",
                Items="0%"
            ),
            element(
                Tag="h5",
                Style="color:peru;text-align:left;margin:8px 1% 8px 1%;",
                Items="current: 0%"
            )
        ]
    )


# ------------ COMBINES BALANCE / CHANGE INTO STATUS SECTION ------------
def my_status():
    return element(
        Style="""
            display:flex;
            flex-wrap:wrap;
            margin:6px 0 0 0;
            justify-content:center;
            border-left:6px solid peru;
            background-color:rgba(25,25,25,.5);
            """,
        Items=[
            my_balance(),
            my_change()
        ]
    )
# -----------------------------------------------------------------------


def my_chart():
    return element(
        ID="budgetChart",
        Tag="canvas",
        Style="""
            width:300px;
            height:300px;
            margin:32px 0 16px 0;
        """
    )


def my_chart_key():

    def key_item(label, color):
        return """
        <div style='display:flex;margin:0 0 6px 6px;height:24px;'>
            <span style='display:inline-block;width:20px;background-color:{color};margin:0 6px 6px 6px;'>
            &nbsp;</span>
            <p>{label}</p>
        </div>  
        """.format(color=color, label=label)

    return element(
        ID="budgetChartKey",
        Tag="div",
        Style="""
            align-content:center;
            justify-content:center;
            display:flex;
            flex-wrap:wrap;
            max-width:400px;
            margin:16px 0 32px 0;
        """,
        Items=[
            key_item(color='#937e88', label='housing'),
            key_item(color='#57d9ff', label='savings'),
            key_item(color='#f16e23', label='utility'),
            key_item(color='#fde23e', label='entertainment'),
            key_item(color='#009933', label='food')
        ]
    )


# -----------------------------------------------------------------------
def my_status_chart():
    return element(
        ID="status-chart",
        Tag="div",
        Style="""
            justify-content:center;
            align-content:center;
            display:flex;
            flex-wrap:wrap;
            width:100%;
            margin:32px 0 32px 0;
        """,
        Items=[
            my_chart(),
            script(
                function='chart',
                parameters='''
                    `budgetChart`,
                    {
                        "food & drink": 1,
                        "entertainment": 2,
                        "utility": 3,
                        "savings": 4,
                        "housing": 5
                    },
                    0.5,
                    `budgetChartKey`
                ''',
                addon=True
            ),
            my_chart_key()
        ]
    )
# -----------------------------------------------------------------------


def my_incomes():
    return element(
        Style='''
            height:32px;
            width:100%;
            max-width:600px;
        ''',
        Items=[
            """
            <h3 style='margin:6px 6px 6px 6px;'> Describe Income </h3>
            <div style='display:flex;'>
            """,
                "<div style='width:24px;height:28px;margin:2px 2px 2px 2px;'>",
                    svg('cross'),
                "</div>"
                "<input/>",
                "<input/>",
                "<input/>",
                "<div style='width:24px;height:28px;margin:2px 2px 2px 2px;'>",
                    svg('plus'),
                "</div>"
            "</div>"
        ]
    )


def my_expenses():

    def expense(desc=str(), cost=str(), cat=str()):
        return """
            <div style='border-bottom:1px solid grey;padding:3px 3px 3px 3px;display:flex;'>
                <div style='border-right:1px solid grey;width:33%;padding-top:6px;'>""" + desc + """</div>
                <div style='border-right:1px solid grey;width:33%;padding-top:6px;'>""" + cost + """</div>
                <div style='width:33%;padding-top:6px;'>""" + cat + """</div>
            <div style='width:20px;height:20px;padding:4px 4px 4px 4px;'> """ + svg('cross') + """ </div>
            </div>
        """

    return element(
        Items=[
        "<div style='display:flex;min-width:99%;border-bottom:1px solid grey;justify-content:center;align-content:center;text-align:center;padding:2% 0 1% 1%;'>", 
            "<input style='width:25%;' placeholder='description' /><input style='width:25%;' placeholder='amount' />",
            """
            <select style='width:25%;'> 
                <option value=''> housing </option> 
                <option value=''> utility </option> 
                <option value='' selected> entertainment </option> 
                <option value=''> food & drink </option> 
            </select>
            <button style='width:48px;margin:0 1% 0 1%;'>""", 
                svg('plus'), "</button>"
        "</div><div id='expenses'>",
            expense('hello', 'world', '!'),
            expense(),
            expense(),
            expense(),
            expense(),
            expense(),
        "</div>"
        ]
    )


# -----------------------------------------------------------------------
def my_ledger():
    return element(
        Style="""
            display:block;
            padding:1% 1%px 16px 1%;
            justify-content:center;
            border-left:6px solid peru;
            background-color:rgba(20,20,20,.25);",
        """,
        Items=[
        "<div style='display:flex;'>",
            "<div style='width:50%;height:32px;border:2px solid peru;background-color:#F77205;justify-content:center;box-shadow:10px 10px 10px rgba(1,1,1,.8);border-right:0 solid peru'><h2>Income</h2></div>",
            "<div style='width:50%;height:32px;border:2px solid peru;background-color:none;justify-content:center;'><h2 style='color:grey;'>Expenses</h2></div>",
        "</div>",
            my_expenses()
        ]
    )
# -----------------------------------------------------------------------


# Page Content
App.add_elements(
    my_status(),
    my_status_chart(),
    my_ledger()
)

# Page Render
App = App.render()
