const extendWidth = (id, extend) => {
    if (pageWidthExtendedElement !== null && pageWidthExtendedElement !== id){
        document.getElementById(pageWidthExtendedElement).style.minWidth = '0px';
    } else {
        pageWidthExtendedElement = id;
    } if (document.getElementById(id).style.minWidth === extend) {
        document.getElementById(id).style.minWidth = '0px';
    } else {
        document.getElementById(id).style.minWidth = extend;
    }
}