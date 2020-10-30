
function userMenu(){
    udiv = document.getElementById('user-menu');
    ndiv = document.getElementById('no-user-menu');
    if(_token_ !== null && _email_ !== null){
        ndiv.style.display = 'none';
        if(udiv.style.display !== 'block'){
            udiv.style.display = 'block';
        } else {
            udiv.style.display = 'none';
        }
    } else {
        udiv.style.display = 'none';
        if(ndiv.style.display !== 'block'){
            ndiv.style.display = 'block';
        } else {
            ndiv.style.display = 'none';
        }
    }
}
