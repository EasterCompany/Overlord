const _cookie_ = __getCookies__();

function __getCookies__(){
    if (document.cookie.includes(';')) {
        const cookie = document.cookie.split('; ');
        const cookies = {};
        for(i in cookie){
            cookies[cookie[i].split('=')[0]] = cookie[i].split('=')[1];
        };
        return cookies
    } else if (document.cookie.length > 0) {
        const cookie = document.cookie.split('=');
        const cookies = {};
        cookies[cookie[0]] = cookie[1];
        return cookies
    } else {
        return {};
    }
}

console.log(_cookie_);

function __autoLogin__(){
    if('email' in _cookie_ && 'token' in _cookie_){
        console.log('has login');
    }
}

if(document.location.href.includes('/dist?')){
    __autoLogin__();
}
