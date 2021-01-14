
const getServerAdr = () => {
    if (window.location.href === 'http://localhost:8100/'){
        return 'http://localhost:8000/'
    } else {
        return window.location.href
    }
}


const serverAdr = getServerAdr()

export default serverAdr
