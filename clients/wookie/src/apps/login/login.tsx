// React imports
import './login.css';
// Shared library
import { login } from '../../shared/library/local/user';


const UserLogin = () => {

  const onSubmit = async (event:any) => {
    event.preventDefault();
    const email = document.getElementById("email") as HTMLInputElement;
    const pass = document.getElementById("pass") as HTMLInputElement;
    if (email.value === '') email.style.backgroundColor = "rgba(200, 33, 33, 0.25)";
    if (pass.value === '') pass.style.backgroundColor = "rgba(200, 33, 33, 0.25)";
    await login(email.value, pass.value);
    const label = document.getElementById("invalid_label") as HTMLElement;
    label.style.display="block";
  }

  return <div id="login-page">
    <h1> E-PANEL LOGIN </h1>
    <h2> &lt; {window.location.host} &gt; </h2>
    <h3 id="invalid_label" className="label"> Invalid Email & Password Combination. </h3>
    <form onSubmit={onSubmit}>
      <input type="text" id="email" name="email" placeholder="email address"
        onClick={() => {
          const email_el = document.getElementById("email") as HTMLInputElement;
          email_el.style.backgroundColor = "rgba(0,0,0,0)";
      }}/>
      <input type="password" id="pass" name="pass" placeholder="password"
        onClick={() => {
          const pass_el = document.getElementById("pass") as HTMLInputElement;
          pass_el.style.backgroundColor = "rgba(0,0,0,0)";
      }}/>
      <button id="submit"> Login </button>
    </form>
  </div>
}


export default UserLogin;
