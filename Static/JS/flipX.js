const flipY = (id) => {
    if (document.getElementById(id).style.transform !== 'scaleX(-1)'){
        document.getElementById(id).style.transform = 'scaleX(-1)';
    } else {
        document.getElementById(id).style.transform = 'scaleX(1)';
    }
};