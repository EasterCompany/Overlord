
const sanitize = (str) => {
    let r = str
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
    return r
}

export default sanitize
