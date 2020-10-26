from Overlord.Canopy.Core import Document, script
from Overlord.Canopy.Elements import form

App = Document()


def login_form():
    return form(
        """
        <h2 style='text-align:center;font-family:open sans;'> Login </h2>
        <br>
        <br>
        <label for='email'>Email:</label>
        <input type='email' id='email' name='email' placeholder='Email' onclick='document.getElementById(`email`).style.backgroundColor=`rgba(25,25,25,.5)`;'/>
        <br>
        <br>
        <label for='passw'>Password:</label>
        <input type='password' id='passw' name='passw' placeholder='Password' onclick='document.getElementById(`passw`).style.backgroundColor=`rgba(25,25,25,.5)`;'/>
        <br>
        <br>
        <br>
        <button id='login_button' class='button'
            onclick='{onclick}'
            style='
                width:150px;
                margin-left:calc(50% - 75px);
                border-radius:6px;
                background-color:peru;
            '
        >Login</button>
        <br>
        <br>
        <br>
        <div style='display:flex;justify-content:space-around;'>
            <a>forgot password?</a>
        </div>
        <br>
        <div style='display:flex;justify-content:space-around;'>
            <a href='/dist?app=register'>haven't got an account?</a>
        </div>
        """.format(
            onclick=script('loginForm')
        )
    )


App.add_elements(login_form())
App = App.render()
