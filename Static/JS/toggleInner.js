function toggleInner(ID, x, y){
    if(document.getElementById(ID).innerHTML.includes(x)){
        document.getElementById(ID).innerHTML = y;
    } else {
        document.getElementById(ID).innerHTML = x;
    }
}