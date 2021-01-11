
const sanitize = (str) => {
    let r = str
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/ +(?= )/g,'')
        .replace(/(\r\n|\r|\n){3,}/g, '$1\n')
    return r
}

export default sanitize
