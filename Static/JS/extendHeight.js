const extendHeight = (id, extend) => {
    if (pageHeightExtendedElement !== null && pageHeightExtendedElement !== id) {
        document.getElementById(pageHeightExtendedElement).style.minHeight = '0px';
    }
    pageHeightExtendedElement = id;
    if (document.getElementById(id).style.minHeight === extend) {
        document.getElementById(id).style.minHeight = '0px';
    } else {
        document.getElementById(id).style.minHeight = extend;
    }
}