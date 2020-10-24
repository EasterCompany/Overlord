async function loginUser(email, passw){
    function callback(text){
        if(text !== 'success!'){
            alert(text);
        } else {
            alert(text);
            /* window.location.href = '/dist?app=login'; */
        }
    }
    fetch('/user/auth?email=' + email + '&passw=' + passw).then(
        (response) => response.text().then(callback)
    );
};

function loginForm(){
    const email = document.getElementById('email');
    const passw = document.getElementById('passw');
    loginUser(encodeURI(email.value), encodeURI(passw.value));
}