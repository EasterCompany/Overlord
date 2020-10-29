
function __getCookies__(){
    const cookies = {
        email: null,
        token: null
    };
    if (document.cookie.includes(';')) {
        const cookie = document.cookie.split('; ');
        for(i in cookie){
            cookies[cookie[i].split('=')[0]] = cookie[i].split('=')[1];
        };
        return cookies;
    } else if (document.cookie.length > 0) {
        const cookie = document.cookie.split('=');
        cookies[cookie[0]] = cookie[1];
        return cookies;
    }
    return cookies;
}

function __autoLogin__(){
    if(_email_ !== null && _token_ !== null){
        if( window.location.href.includes('/dist?app=login') ||
            window.location.href.includes('/dist?app=register')
        ){
            window.location.href = '/dist?app=budget';
        }
    }
}

function __logout__(){
    const expire = new Date();
    expire.setFullYear(expire.getFullYear() - 1);
    document.cookie = `token=; expires=${expire}; path=/`;
    document.cookie = `email=; expires=${expire}; path=/`;
    window.location.href = '/';
}

const _cookie_ = __getCookies__();
const _token_ = _cookie_['token'];
const _email_ = _cookie_['email'];

if(document.location.href.includes('/dist?')){
    __autoLogin__();
}
