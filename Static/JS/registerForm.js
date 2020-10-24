async function registerUser(email, passw){
    function callback(text){
        if(text !== 'success!'){
            alert(text);
        } else {
            window.location.href = '/dist?app=login';
        }
    }
    fetch('/user/add?email=' + email + '&passw=' + passw).then(
        (response) => response.text().then(callback)
    );
};

function registerForm(){
    const email = document.getElementById('email');
    const passw = document.getElementById('passw');
    const cpass = document.getElementById('cpass');
    if(email.value.includes('@') && email.value.includes('.') && email.value.length >= 5){
        if(passw.value === cpass.value){
            if(passw.value.length >= 8){
                registerUser(
                    encodeURIComponent(email.value), 
                    encodeURIComponent(passw.value)
                )
            } else {
                alert('Password must be at least 8 characters in length.');
                passw.style.backgroundColor = 'rgba(100,5,5,.8)';
                cpass.style.backgroundColor = 'rgba(100,5,5,.8)';
            };
        } else {
            alert('Password fields do not match.');
            passw.style.backgroundColor = 'rgba(100,5,5,.8)';
            cpass.style.backgroundColor = 'rgba(100,5,5,.8)';
        };
    } else {
        alert('Please enter a valid email address.');
        email.style.backgroundColor = 'rgba(100,5,5,.8)';
    };
    return false;
};
