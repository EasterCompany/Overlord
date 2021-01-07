import './navbar.css'
import logo from '../../../assets/logo.svg'
import bell from '../../../assets/icons/bell.svg'
import chat from '../../../assets/icons/chat.svg'
import menu from '../../../assets/icons/menu.svg'
import rightAIcon from '../../../assets/icons/to_right.svg'
import searchIcon from '../../../assets/icons/search.svg'
import newMsgIcon from '../../../assets/icons/plus.svg'
import fulScrIcon from '../../../assets/icons/fullscreen.svg'
import profileIcon from '../../../assets/icons/user.svg'
import appsIcon from '../../../assets/icons/folder.svg'
import settingsIcon from '../../../assets/icons/spanner.svg'
import logoutIcon from '../../../assets/icons/close.svg'


const navbarNotification = () => {
    return `<div>hello!</div>`
}


const navbarMenuButton = (title, onClickFunction, icon, expands) => {
    let ifExpands = `<div style='min-width:10%;'></div>`

    if (expands) {
        ifExpands = `<img
            src=${rightAIcon}
            style='width:10%;height:28px;margin-top:8px;'
        />`
    }

    return `
    <div class="global-navbar-menu-button" onClick="${onClickFunction}()">
        <img src=${icon} style='width:10%;' />
        <h3 style='pointer-events:none;width:80%;margin-top:12px;'>${title}</h3>
        ${ifExpands}
    </div>
    `
}


const navbarInboxMsg = (dp, name, preview, status, timestamp) => {
    let detailStyle = ''
    let statusText = ''

    if (status === 0) {
        detailStyle = 'background-color:rgba(.2,.2,.2,.1);'
        statusText = 'New'
    }
    if (status === 1) { statusText = 'Read' }
    if (status === 2) { statusText = 'Sent' }
    if (status === 3) { statusText = 'Seen' }

    if (name.length > 26) {name = name.substring(0, 24) + '..'}

    return `
    <div class='global-navbar-inbox-msg'>
        <img src='${dp}' style='width:15%;'/>
        <div
            class='global-navbar-inbox-msg-detail'
            style='${detailStyle}'
        >
            <h4 style='margin:6px 3px 6px 3px;user-select:none;'> ${name} </h4>
            <h6 style='margin:6px 6px 0 6px;user-select:none;'> ${preview} </h6>
        </div>
        <div style='display:block'>
            <p class='global-navbar-inbox-msg-status'> ${statusText} </p>
            <p class='global-navbar-inbox-msg-status'> ${timestamp} </p>
        </div>
    </div>
    `
}


const navbarMenuHTML = {

    /* --------------------------------------------------------------------- */
    menu:`
        ${navbarMenuButton("Profile", "console.log", profileIcon, false)}
        ${navbarMenuButton("Apps", "console.log", appsIcon, true)}
        ${navbarMenuButton("Settings", "console.log", settingsIcon, true)}
        ${navbarMenuButton("Logout", "console.log", logoutIcon, false)}
        <div style='
            margin:6px 0 6px 0;
            text-align:center;
            color:grey;
        '>
            <a class='global-navbar-menu-footer' href='/'> Privacy </a> ·
            <a class='global-navbar-menu-footer' href='/'> Cookies </a> ·
            <a class='global-navbar-menu-footer' href='/'> Terms </a> ·
            <a class='global-navbar-menu-copyright'> Easter Company © 2021 </a>
        </div>
    `,

    /* --------------------------------------------------------------------- */
    inbox:`
    <div style='
        display:flex;
        margin-bottom:8px;
        justify-content:space-around;
    '>
        <div style='display:flex;margin-top:6px;'>
            <img src=${searchIcon} style='
                width:28px;
                height:28px;
                margin-top:8px;
                margin-left:12px;
            ' />
            <input
                class='global-navbar-inbox-search'
                placeholder='Search contacts'
                minlength='1'
            />
        </div>
        <div style='display:flex;margin-top:6px;'>
            <img src=${newMsgIcon} style='
                width:28px;
                height:28px;
                margin: 8px 12px 0 8px;
                cursor: pointer;
            ' />
            <img src=${fulScrIcon} style='
                width:28px;
                height:28px;
                margin-top:8px;
                margin-right:12px;
                cursor: pointer;
            ' />
        </div>
    </div>
    <div class='global-navbar-inbox'>
        ${navbarInboxMsg(logo, 'John Smith', 'This is an unread message!', 0, '1m')}
        ${navbarInboxMsg(logo, 'Jane Doe', 'This is a read message.', 1, '2h')}
        ${navbarInboxMsg(logo, 'Jon Snow', 'This is a sent message.', 2, '3d')}
        ${navbarInboxMsg(logo, 'Julius Ceaser', 'This is a seen message.', 3, '1W')}
        ${navbarInboxMsg(logo, 'Julius Salad', 'This is 1 month old.', 3, '2M')}
        ${navbarInboxMsg(logo, 'Jon Targaryen', 'This is 1 year old.', 3, '1Y')}
        ${navbarInboxMsg(logo, 'ThisIsA ReallyLongName', 'This is 1 month old.', 3, '1M')}
        ${navbarInboxMsg(logo, 'ThisIsA ReallyReallyLongName', 'This is 1 month old.', 3, '1M')}
        ${navbarInboxMsg(logo, 'ThisIsA ReallyReallyReallyReallyLongName', 'This is 1 month old.', 3, '1M')}
    </div>
    `,

    /* --------------------------------------------------------------------- */
    notifications: `
        ${navbarNotification()}
        ${navbarNotification()}
        ${navbarNotification()}
    `

}


let selectedNavbarMenu = null


const toggleNavbarMenu = (menuType) => {
    const menu = document.getElementById('global-navbar-menu')

    if (menu.style.display === 'block' && selectedNavbarMenu === menuType) {
        menu.style.display = 'none'
    } else {
        menu.style.display = 'block'
    }

    selectedNavbarMenu = menuType

    if (menuType) {
        menu.innerHTML = `
            <div style='background-color:black;'>
                <h6 style='
                    color:white;
                    text-align:left;
                    margin: 0 0 0 6px;
                '>
                    ${selectedNavbarMenu.toUpperCase()}
                </h6>
            </div>
            <div class='global-navbar-menu-content'>
                ${navbarMenuHTML[selectedNavbarMenu]}
            </div>
        `
    }
}


const RedirectHome = () => {
    document.location.href = '/'
}


const popAppID = [
    'journal',
    'finance',
    'discover'
]


const popAppSelect = (selected) => {
    let targetBtn = null
    let targetBod = null

    for(const popApp in popAppID){
        targetBtn = 'global-navbar-popapp-' + popAppID[popApp]
        targetBod = 'popApp-container-' + popAppID[popApp]

        if (popAppID[popApp] === selected){
            document.getElementById(
                targetBod
            ).className = 'popApp-container-selected'
            document.getElementById(
                targetBtn
            ).className = 'global-navbar-popapp-selected'
        } else {
            document.getElementById(
                targetBod
            ).className = 'popApp-container'
            document.getElementById(
                targetBtn
            ).className = 'global-navbar-popapp'
        }

    }

}


/*
    THESE FUNCTIONS ARE DECLARED TO AVOID USE OF ARROW FUNCTIONS INSIDE JSX
    ELEMENTS IN THE NAVBAR/TRAY -> WHICH WOULD CAUSE BAD MEMORY PERFORMANCE

    [Arrow functions inside onClick arguments create a new function on each
     use.]
*/
const toggleInboxTray = () => {toggleNavbarMenu('inbox')}
const toggleMenuTray  = () => {toggleNavbarMenu('menu')}
const toggleNotiTray = () => {toggleNavbarMenu('notifications')}


const popAppSelectJournal = () => {popAppSelect('journal')}
const popAppSelectFinance = () => {popAppSelect('finance')}
const popAppSelectDiscover = () => {popAppSelect('discover')}


/*
    EXPORTED REACT ELEMENT (NAVBAR) CONTAINS ALL FUNCTIONALITY FROM THIS FILE
    EMBEDDED DIRECTLY OR RECURSIVELY WITHIN
*/
const Navbar = () => {
    return <div id='document-header' className='document-header'>
        <div className='global-navbar'>
            <div className='global-navbar-left' onClick={RedirectHome}>
                <img
                    src={logo}
                    className='global-navbar-logo'
                    alt='Easter Company Logo'
                />
                <h1 className='global-site-header'> Easter Company </h1>
            </div>
            <div className='global-navbar-right'>
                <img className='global-navbar-button'
                    src={bell} alt='Notification Button'
                    onClick={toggleNotiTray}
                />
                <img className='global-navbar-button'
                    src={chat} alt='Messages Button'
                    onClick={toggleInboxTray}
                />
                <img className='global-navbar-button'
                    src={menu} alt='Menu Button'
                    onClick={toggleMenuTray}
                />
            </div>
            <div className='global-navbar-divider'></div>
        </div>
        <div className='global-navbar-menu-container'>
            <div className='global-navbar-menu-spacer' />
            <div className='global-navbar-menu' id='global-navbar-menu' />
        </div>
        <div className='global-navbar-pop'>
            <div
                id='global-navbar-popapp-journal'
                className='global-navbar-popapp-selected'
                onClick={popAppSelectJournal}
            > <span style={{userSelect:'none'}}> Journal </span> </div>
            <div
                id='global-navbar-popapp-finance'
                className='global-navbar-popapp'
                onClick={popAppSelectFinance}
            > <span style={{userSelect:'none'}}> Finance </span> </div>
            <div
                id='global-navbar-popapp-discover'
                className='global-navbar-popapp'
                onClick={popAppSelectDiscover}
            > <span style={{userSelect:'none'}}> Discover </span> </div>
        </div>
    </div>
}


export default Navbar
