import './navbar.css'
import logo from '../../../assets/logo.svg'
import bell from '../../../assets/icons/bell.svg'
import chat from '../../../assets/icons/chat.svg'
import menu from '../../../assets/icons/menu.svg'


const navbarMenuButton = (title, onClickFunction) => {
    return `
        <div class="global-navbar-menu-button" onClick="${onClickFunction}()">
            <h3 style='pointer-events:none;'>${title}</h3>
        </div>
    `
}


const navbarMenuHTML = {
    menu:
        `
        ${navbarMenuButton("Profile", "console.log")}
        <hr>
        ${navbarMenuButton("Apps", "console.log")}
        <hr>
        ${navbarMenuButton("Settings", "console.log")}
        <hr>
        ${navbarMenuButton("Logout", "console.log")}
        <div style='
            text-align:center;
            margin:0 0 -12px 0;
            color:grey;
            background-color:black;
        '>
            <a class='global-navbar-menu-footer' href='/'> Privacy </a> ·
            <a class='global-navbar-menu-footer' href='/'> Cookies </a> ·
            <a class='global-navbar-menu-footer' href='/'> Terms </a> ·
            <a class='global-navbar-menu-copyright'> Easter Company © 2021 </a>
        </div>
        `,
    inbox:
        `
        <h2> Hello Inbox! </h2>
        `,
    notifications:
        `
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
                <h6 style='color:white;text-align:left;margin-bottom:0;'>
                    ${selectedNavbarMenu.toUpperCase()}
                </h6>
            </div>
        ` + navbarMenuHTML[selectedNavbarMenu]
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
            </div>
            <div className='global-navbar-menu' id='global-navbar-menu'></div>
            <div className='global-navbar-divider'> &nbsp; </div>
        </div>
    )
}


export default Navbar;
