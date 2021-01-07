import { prefixedNumeral } from './math.js'

const _ = new Date()
const months = [
    'January', 'Febuary', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]


const date = () => {
    return _.getDate() + '/' + months[_.getMonth()] + '/' + _.getFullYear()
}


const shortDate = () => {
    return prefixedNumeral(_.getDate()) + ' ' + months[_.getMonth()]
}


const time = () => {
    return _.getHours() + ':' + _.getMinutes()
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
