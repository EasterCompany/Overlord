const __toggledUI_element__ = {'id':'','inner':'','display':''};
function toggleUI(ID, x, y, display=String()) {
    if(ID !== __toggledUI_element__['id'] && __toggledUI_element__['id'] !== '') {
        document.getElementById(__toggledUI_element__['id']).innerHTML = __toggledUI_element__['inner'];
    };
    __toggledUI_element__['id']=ID;
    __toggledUI_element__['inner']=x;
    if(document.getElementById(ID).innerHTML.includes(x)){
        document.getElementById(ID).innerHTML = y;
        document.getElementById(display).style.display = 'none';
    } else {
        document.getElementById(ID).innerHTML = x;
        document.getElementById(display).style.display = 'block';
    };
};
