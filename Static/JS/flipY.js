const flipY = (id) => {
    if (document.getElementById(id).style.transform !== 'scaleY(-1)'){
        document.getElementById(id).style.transform = 'scaleY(-1)';
    } else {
        document.getElementById(id).style.transform = 'scaleY(1)';
    }
};