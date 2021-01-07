

const prefixedNumeral = (n) => {
    n = String(n)
    if (n.endsWith('11') || n.endsWith('12') || n.endsWith('13')) {
        return n + 'th'
    } else if (n.endsWith('1')) {
        return n + 'st'
    } else if (n.endsWith('2')) {
        return n + 'nd'
    } else if (n.endsWith('3')) {
        return n + 'rd'
    } else {
        return n + 'th'
    }
}


export {
    prefixedNumeral,
}
