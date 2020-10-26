from Overlord.Canopy.Core import Document, script
from Overlord.Canopy.Elements import form

App = Document()


def register_form():
    return form("""
        <h2 style='text-align:center;font-family:open sans;'> New Account </h2>
        <br>
        <br>
        <label for='email'>Email:</label><br/>
        <input type='email' id='email' name='email' placeholder='Email' onclick='document.getElementById(`email`).style.backgroundColor=`rgba(25,25,25,.5)`;'/>
        <br>
        <br>
        <label for='passw'>Password:</label><br/>
        <input type='password' id='passw' name='passw' placeholder='Password' onclick='document.getElementById(`passw`).style.backgroundColor=`rgba(25,25,25,.5)`;'/>
        <br>
        <br>
        <label for='cpass'>Confirm Password:</label><br/>
        <input type='password' id='cpass' name='cpass' placeholder='Password again...' onclick='document.getElementById(`cpass`).style.backgroundColor=`rgba(25,25,25,.5)`;'/>
        <br>
        <br>
        <br>
        <button id='register_button' class='button'
            onclick='{onclick}'
            style='
                width:150px;
                margin-left:calc(50% - 75px);
                border-radius:6px;
                background-color:peru;
            ' 
        >Sign up!</button>
        <br>
        <br>
        <br>
        <div style='display:flex;justify-content:space-around;'>
            <a href='/dist?app=login'>already have an account?</a>
        </div>
        <br>
        """.format(
            onclick=script('registerForm')
        )
    )


App.add_elements(
    register_form()
)
App = App.render()
