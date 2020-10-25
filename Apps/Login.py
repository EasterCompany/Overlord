from Overlord.Canopy.Core import Document, script
from Overlord.Canopy.Elements import form

App = Document()


def login_form():
    return form(
        """
        <h2 style='text-align:center;font-family:open sans;'> Login </h2>
        <br>
        <label for='email'>Email:</label>
        <input type='email' id='email' name='email' placeholder='Email' onclick='document.getElementById(`email`).style.backgroundColor=`rgba(25,25,25,.5)`;'/>
        <br>
        <br>
        <label for='passw'>Password:</label>
        <input type='password' id='passw' name='passw' placeholder='Password' onclick='document.getElementById(`passw`).style.backgroundColor=`rgba(25,25,25,.5)`;'/>
        <br>
        <br>
        <button id='login_button' class='button'
            onclick='""" + script('loginForm') + """'
            style='
                width:150px;
                margin-left:75px;
                border-radius:6px;
                background-color:peru;
            '
        >Login</button>
        <br>
        <br>
        <a style='margin-left:30%;'>forgot password?</a>
        <br>
        <br>
        <a style='margin-left:21.5%;' href='/dist?app=register'>haven't got an account?</a>
        """
    )


App.add_elements(login_form())
App = App.render()
