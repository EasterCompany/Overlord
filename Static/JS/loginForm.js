
function loginForm(){
    const email = document.getElementById('email').value;
    const passw = document.getElementById('passw').value;

    function callback(text){
        if(text !== ''){
            let expire = new Date();
            expire.setSeconds(expire.getSeconds() + (60 * 60 * 24 * 30));
            document.cookie = `email=${email}; expires=${expire}; path=/`;
            document.cookie = `token=${text}; expires=${expire}; path=/`;
            window.location.href = '/dist?app=library';
        } else {
            alert('Invalid email and password combination.');
        }
    }

    fetch('/user/auth?email=' +
            encodeURIComponent(email) +
            '&passw=' + encodeURIComponent(passw)
        ).then(
            (response) => response.text().then(callback)
    );
};
