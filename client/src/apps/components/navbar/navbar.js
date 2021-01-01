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


const navbarInboxMsg = (dp, name, preview, status) => {
    const pinStatus = "<b style='font-size:110%;'>·</b>"
    let detailStyle = ''
    let statusText = '...'

    if (status === 0) {
        detailStyle = 'background-color:rgba(.2,.2,.2,.1);'
        statusText = pinStatus
    }
    if (status === 1) { statusText = 'Read' }
    if (status === 2) { statusText = 'Sent' }
    if (status === 3) { statusText = pinStatus }

    return `
    <div class='global-navbar-inbox-msg'>
        <img src='${dp}' style='width:15%;'/>
        <div
            class='global-navbar-inbox-msg-detail'
            style='${detailStyle}'
        >
            <h4 style='margin:6px 6px 6px 6px;'> ${name} </h4>
            <h6 style='margin:6px 6px 0 6px;'> ${preview} </h6>
        </div>
        <p class='global-navbar-inbox-msg-status'> ${statusText} </p>
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
    <div style='display:flex;justify-content:space-around;margin-bottom:8px;'>
        <div style='display:flex;margin-top:6px;'>
            <img src=${searchIcon} style='
                width:28px;
                height:28px;
                margin-top:8px;
                margin-left:12px;
            ' />
            <input class='global-navbar-inbox-search' placeholder='Search contacts' />
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
        ${navbarInboxMsg(logo, 'John Smith', 'This is an unread message!', 0)}
        ${navbarInboxMsg(logo, 'Jane Doe', 'This is a read message.', 1)}
        ${navbarInboxMsg(logo, 'Jon Snow', 'This is a sent message.', 2)}
        ${navbarInboxMsg(logo, 'Julius Ceaser', 'This is a sent/read message.', 3)}
    </div>
    `,

    /* --------------------------------------------------------------------- */
    notifications:`
        <h2> Hello Notifications! </h2>
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


/*
    THESE FUNCTIONS ARE DECLARED TO AVOID USE OF ARROW FUNCTIONS INSIDE JSX
    ELEMENTS IN THE NAVBAR/TRAY -> WHICH WOULD CAUSE BAD MEMORY PERFORMANCE

    [Arrow functions inside onClick arguments create a new function on each
     use.]
*/
const toggleInboxTray = () => {toggleNavbarMenu('inbox')}
const toggleMenuTray  = () => {toggleNavbarMenu('menu')}
const toggleNotiTray = () => {toggleNavbarMenu('notifications')}


const RedirectHome = () => {
    document.location.href = '/'
}


/*
    EXPORTED REACT ELEMENT (NAVBAR) CONTAINS ALL FUNCTIONALITY FROM THIS FILE
    EMBEDDED DIRECTLY OR RECURSIVELY WITHIN
*/
const Navbar = () => {
    return (
        <div className='document-header'>
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
                <div className='global-navbar-menu-spacer'></div>
                <div className='global-navbar-menu' id='global-navbar-menu' />
            </div>
            <div className='global-navbar-pop'>
                <div className='global-navbar-popapp-selected'> Journal </div>
                <div className='global-navbar-popapp'> Finance </div>
                <div className='global-navbar-popapp'> Discover </div>
            </div>
            <div style={{minHeight: '2000px'}} />
        </div>
    )
}


export default Navbar;
