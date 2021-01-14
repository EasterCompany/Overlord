import { prefixedNumeral } from './math.js'

const _ = new Date()
const months = [
    'January', 'Febuary', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]


const date = (d=_) => {
    return d.getDate() + '/' + months[d.getMonth()] + '/' + d.getFullYear()
}


const shortDate = (d=_) => {
    return prefixedNumeral(d.getDate()) + ' ' + months[d.getMonth()]
}


const time = (d=_) => {
    return d.getHours() + ':' + d.getMinutes()
}


const dateTime = () => {
    return date() + ' ' + time()
}


export default dateTime
export {
    date,
    time,
    shortDate
}
