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
                Items="+ 0.00 pm"
            )
        ]
    )


def my_change():
    return element(
        Style="display:block;width:106px;",
        Items=[
            element(
                Tag="h5",
                Style="color:peru;text-align:right;margin:8px 1% 8px 1%;",
                Items="AVG CHANGE"
            ),
            element(
                Tag="h1",
                Style="color:peru;text-align:right;margin:8px 1% 8px 1%;",
                Items="0%"
            )
        ]
    )


# ------------ COMBINES BALANCE / CHANGE INTO STATUS SECTION ------------
def my_status():
    return element(
        Style="""
            display:flex;
            flex-wrap:wrap;
            margin:0 auto;
            max-width:800px;
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
            key_item(color='#009933', label='supply')
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
                        "supply": 1,
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
        ID='incomes',
        Style='display:none;',
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

    def expense(desc=str(), cost=str(), occr=str(), cat=str()):
        return """
            <div style='border-bottom:1px solid grey;padding:3px 3px 3px 3px;display:flex;'>
                <div style='border-right:1px solid grey;width:25%;padding-top:6px;overflow:hidden;font-size:.8rem;'>""" + desc + """</div>
                <div style='border-right:1px solid grey;width:25%;padding-top:6px;overflow:hidden;font-size:.8rem;'>""" + cost + """</div>
                <div style='border-right:1px solid grey;width:25%;padding-top:6px;overflow:hidden;font-size:.8rem;'>""" + occr + """</div>
                <div style='border-right:1px solid grey;width:25%;padding-top:6px;overflow:hidden;font-size:.8rem;'>""" + cat + """</div>
            <div style='width:20px;height:20px;padding:4px 4px 4px 4px;'> """ + svg('cross') + """ </div>
            </div>
        """

    return element(
        ID='expenses',
        Items=[
        """<div style='display:flex;height:28px;border-bottom:1px solid grey;
            justify-content:center;align-content:center;text-align:center;
            padding:2% 0 2% 0;margin-left:8px;'>""", 
            "<input style='width:25%;' placeholder='description' />",
            "<input style='width:25%;' placeholder='amount' />",
            """
            <select style='width:25%;'> 
                <option value=''> daily </option> 
                <option value=''> weekly </option> 
                <option value='' selected> monthly </option> 
                <option value=''> annual </option> 
            </select>
            """,
            """
            <select style='width:25%;'> 
                <option value=''> housing </option> 
                <option value=''> utility </option> 
                <option value='' selected> entertainment </option> 
                <option value=''> supply </option> 
            </select>
            <div style='width:28px;height:28px;margin-right:8px;'>""", 
                svg('plus'), "</div>"
        "</div><div id='expenses'>",
            expense('food', '7.00', 'daily', 'supply'),
            expense('amazon prime', '3.00', 'monthly', 'entertainment'),
            expense('rent', '150.00', 'monthly', 'housing'),
        "</div>"
        ]
    )


# -----------------------------------------------------------------------
def my_ledger():
    return element(
        Style="""
            display:block;
            margin:0 auto;
            max-width:800px;
            padding:1% 1%px 16px 1%;
            border-left:6px solid peru;
            background-color:rgba(20,20,20,.25);",
        """,
        Items=[
        "<div style='display:flex;'>",
            """
        <div id='income-tab' style='
            width:50%;height:32px;cursor:pointer;
            border:2px solid peru;background-color:none;color:grey;
            justify-content:center;font-size:1.5rem;padding-top:3px;' 
            onclick='""" + script('ba_loadIncome') + """'>Income</div>
            """,
            """
        <div id='expense-tab' style='
            width:50%;height:32px;cursor:pointer;
            border:2px solid peru;background-color:#F77205;
            justify-content:center;box-shadow:10px 10px 10px rgba(1,1,1,.8);
            border-left:0 solid peru;font-size:1.5rem;padding-top:3px;'
            onclick='""" + script('ba_loadExpense') + """'>Expense</div>
            """,
        "</div><div id='ie-content-section'>",
            my_expenses(),
            my_incomes(),
        "</div>"
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
