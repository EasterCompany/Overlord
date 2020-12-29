import './navbar.css'
import logo from '../../../assets/logo.svg'
import bell from '../../../assets/icons/bell.svg'
import chat from '../../../assets/icons/chat.svg'
import menu from '../../../assets/icons/menu.svg'

let selectedNavbarMenu = null


const ToggleNavbarMenu = (menuType) => {
    const menu = document.getElementById('global-navbar-menu')
    if (menu.style.display === 'block' && selectedNavbarMenu === menuType) {
        menu.style.display = 'none'
    } else {
        menu.style.display = 'block'
    }
    selectedNavbarMenu = menuType
}


const RedirectHome = () => {
    document.location.href = '/'
}


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
                        onClick={
                            () => {
                                ToggleNavbarMenu('notification')
                            }
                        }
                    />
                    <img className='global-navbar-button'
                        src={chat} alt='Messages Button'
                        onClick={
                            () => {
                                ToggleNavbarMenu('chat')
                            }
                        }
                    />
                    <img className='global-navbar-button'
                        src={menu} alt='Menu Button'
                        onClick={
                            () => {
                                ToggleNavbarMenu('menu')
                            }
                        }
                    />
                </div>
            </div>
            <div className='global-navbar-menu' id='global-navbar-menu'></div>
            <div className='global-navbar-divider'> &nbsp; </div>
        </div>
    )
}


export default Navbar;
