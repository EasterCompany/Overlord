import './navbar.css'
import logo from '../../../assets/logo.svg'
import bell from '../../../assets/icons/bell.svg'
import chat from '../../../assets/icons/chat.svg'
import menu from '../../../assets/icons/menu.svg'

const RedirectHome = () => {
    document.location.href = '/'
}

const Navbar = () => {
    return (
        <div className='global-navbar'>
            <div className='global-navbar-left' onClick={RedirectHome}>
                <img src={logo} className='app-logo' alt='Easter Company Logo' />
                <h1 className='site-header'> Easter Company </h1>
            </div>
            <div className='global-navbar-right'>
                <img className='global-navbar-button'
                    src={bell} alt='Notification Button' />
                <img className='global-navbar-button'
                    src={chat} alt='Messages Button' />
                <img className='global-navbar-button'
                    src={menu} alt='Menu Button' />
            </div>
        </div>
    );
}

export default Navbar;
