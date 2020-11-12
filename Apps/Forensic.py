# Page Imports
from Overlord.Canopy.Core import Document, script
from Overlord.Canopy.Elements import element
from Overlord.Canopy.Image import svg

# Page Root
App = Document()


# Page Objects
def my_balance():
    return element(
        Style="""
            display:block;
            width:190px;
        """,
        Items=[
            element(
                Tag="h5",
                Style="""
                    color:peru;
                    text-align:left;
                    margin:8px 1% 8px 1%;
                """,
                Items="SAVING"
            ),
            element(
                Tag="div",
                Style="""
                    display:flex;
                    margin:8px 1% 8px 1%;
                """,
                Items=[
                    "<h1 style='color:orange;text-align:left;'> £0. </h1>",
                    "<h3 style='color:orange;text-align:left;margin-top:15px;'> 00 </h3>"
                ]
            )
        ]
    )


def my_change():
    return element(
        Style="display:block;width:106px;",
        Items=[
            element(
                Tag="h5",
                Style="""
                    color:peru;
                    text-align:right;
                    margin:8px 1% 8px 1%;
                """,
                Items="PER MONTH"
            ),
            element(
                Tag="h1",
                Style="""
                    color:peru;
                    text-align:right;
                    margin:8px 1% 8px 1%;
                """,
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
            box-shadow: 1px 1px 32px rgba(1,1,1,1);
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
            key_item(color='#937e88', label='Housing'),
            key_item(color='#57d9ff', label='Savings'),
            key_item(color='#f16e23', label='Utility'),
            key_item(color='#fde23e', label='Leisure'),
            key_item(color='#009933', label='Supply')
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
                        "Supply": 1,
                        "Leisure": 2,
                        "Utility": 3,
                        "Savings": 4,
                        "Housing": 5
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
        Items="""
        <div style='
            display:flex;
            height:28px;
            border-bottom:1px solid grey;
            justify-content:center;
            align-content:center;
            text-align:center;
            padding:5% 0 5% 0;
        '>
            <input id='expense_desc' style='width:25%;' placeholder='description' maxlength='24'/>
            <input id='expense_cost' type='number' step='0.01' style='width:25%;' placeholder='cost'/>
            <select id='expense_occr' style='width:25%;'>
                <option value='Daily'> Daily </option>
                <option value='Weekly'> Weekly </option>
                <option value='Monthly' selected> Monthly </option>
                <option value='Annual'> Annual </option>
            </select>
            <select id='expense_cat' style='width:25%;'>
                <option value='Housing'> Housing </option>
                <option value='Utility'> Utility </option>
                <option value='Leisure' selected> Leisure </option>
                <option value='Supply'> Supply </option>
            </select>
            <div
                style='width:28px;height:28px;margin-right:8px;'
                onclick='""" + script('ba_addExpense') +"""'
            >""" + svg('plus') + """</div>
        </div>
        <div id='expenses'> </div>
        """
    )


# -----------------------------------------------------------------------
def my_ledger():
    return element(
        Style="""
            display:block;
            margin:0 auto;
            margin-bottom: 64px;
            max-width:800px;
            font-family:open sans;
            padding:0 1% 1% 1%;
            border-left:6px solid peru;
            background-color:rgba(20,20,20,.25);
            box-shadow: 1px 1px 32px rgba(1,1,1,1);
        """,
        Items="""
        <div style='display:flex;'>
            <div id='income-tab' style='
                width:50%;height:32px;cursor:pointer;
                border-bottom:2px solid peru;background-color:none;color:grey;
                justify-content:center;font-size:1.5rem;'
                onclick='""" + script('ba_loadIncome') + """'>Income</div>
            <div id='expense-tab' style='
                width:50%;height:32px;cursor:pointer;
                border-bottom:2px solid peru;background-color:#F77205;font-size:1.5rem;
                justify-content:center;box-shadow:10px 10px 10px rgba(1,1,1,.8);'
                onclick='""" + script('ba_loadExpense') + """'>Expense</div>
        </div>
        <div id='ie-content-section'>
            """ + my_expenses() + """
            """ + my_incomes() + """
        </div>
        """
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
