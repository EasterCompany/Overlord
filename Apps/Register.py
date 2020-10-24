from Overlord.Canopy.Core import Document, script
from Overlord.Canopy.Elements import form

App = Document()


def register_form():
    return form(
        """
        <label for='email'>Email:</label>
        <input type='email' id='email' name='email' placeholder='Email' onclick='document.getElementById(`email`).style.backgroundColor=`rgba(25,25,25,.5)`;'/>
        <br>
        <br>
        <label for='passw'>Password:</label>
        <input type='password' id='passw' name='passw' placeholder='Password' onclick='document.getElementById(`passw`).style.backgroundColor=`rgba(25,25,25,.5)`;'/>
        <br>
        <br>
        <label for='cpass'>Confirm Password:</label>
        <input type='password' id='cpass' name='cpass' placeholder='Password again...' onclick='document.getElementById(`cpass`).style.backgroundColor=`rgba(25,25,25,.5)`;'/>
        <br>
        <br>
        <button id='register_button' class='button'
            onclick='""" + script('registerForm') + """'
            style='
                width:150px;
                margin-left:75px;
                border-radius:6px;
                background-color:peru;
            ' 
        >Sign up!</button>
        <br>
        <br>
        <a style='margin-left:18%;' href='/dist?app=login'>already have an account?</a>
        <br>
        """
    )


App.add_elements(register_form())
App = App.render()
