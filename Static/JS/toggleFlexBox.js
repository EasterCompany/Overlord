const toggleFlexBox = (id) => {
    if (document.getElementById(id).style.display === 'flex'){
        document.getElementById(id).style.display = 'none';
    } else {
        document.getElementById(id).style.display = 'flex';
    }
};