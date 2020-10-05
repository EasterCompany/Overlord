const random = (ID, list) => {
    const randomNumber = (min, max) => {
        return Math.floor(Math.random() * (max - min) + min); 
    };
    document.getElementById(ID).innerHTML = list[randomNumber(0, list.length)];
};