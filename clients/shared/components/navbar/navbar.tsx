// React
import { useState, useRef } from 'react';
// Assets
import EmailSVG from '../../assets/icons/email.svg';
import KeySVG from '../../assets/icons/key.svg';
// Library
import { Link } from '../routes/routes';
import { user, login } from '../../library/user';

const NavBarBreakpoint = 1085;


const NavBarLinks = () => {
  return <>
    <a href='/'>Home</a>
    <a href='/books'>Books</a>
    <a href='/overlord'>Overlord</a>
    <a href='/e-panel'>E-Panel</a>
  </>
}


const Navbar = () => {
  const [ showLoginFail, setLoginFail ] = useState(false);
  const [ showLoginModal, setLoginModal ] = useState(false);
  const [ showInviteFail, setInviteFail ] = useState(false);
  const [ showRegisterModal, setRegisterModal ] = useState(false);
  const [ burgerMenuOpen, setBurgerMenuOpen ] = useState(false);
  const [ showBurgerMenuIcon, setBurgerMenuIcon ] = useState(window.innerWidth < NavBarBreakpoint);
  const currentDate = new Date();

  window.addEventListener('resize', () => {
    if (window.innerWidth >= NavBarBreakpoint) {
      setBurgerMenuIcon(false);
      setBurgerMenuOpen(false);
    }
    else if (!showBurgerMenuIcon) {
      setBurgerMenuIcon(true);
    }
  });

  const UserModalFooter = () => {
    return <div className="nav-user-modal-foot">
      © Easter Company {currentDate.getFullYear()}
    </div>
  }

  const closeAllModals = () => {
    setLoginFail(false);
    setLoginModal(false);
    setInviteFail(false);
    setRegisterModal(false);
    setBurgerMenuOpen(false);
  }

  const LoginModal = () => {
    const userEmailInput = useRef<HTMLInputElement>(null);
    const userPassInput = useRef<HTMLInputElement>(null);
    const attemptLogin = () => {
      if (userEmailInput.current !== null && userPassInput.current !== null) login(
        userEmailInput.current.value,
        userPassInput.current.value,
        (resp:any) => setLoginFail(true),
        (resp:any) => {window.location.reload()}
      );
    }

    return <>
      <div className="nav-user-modal-bg" onClick={closeAllModals}/>
      <div className="nav-user-modal" style={{paddingTop: '32px'}}>
        { showBurgerMenuIcon ?
            <></>
          :
            <div className="nav-user-modal-head">
              <i className="fa-solid fa-times nav-user-modal-close" onClick={closeAllModals}/>
            </div>
        }
          <h1 style={ showLoginFail ? { marginBottom: '5%' } : { marginBottom: '10%' } }> Welcome back! </h1>
          { showLoginFail ?
              <div className="nav-user-modal-login-error">
                You need to enter a valid email & password combination.
              </div>
            :
              <></>
          }
          <p><img src={EmailSVG} alt="email" width="16px"/>Email</p>
          <input id="email" name="email" type="email" ref={userEmailInput}/>
          <p><img src={KeySVG} alt="password" width="16px"/>Password</p>
          <input id="password" name="password" type="password" ref={userPassInput}/>
          <div style={{ marginTop: '5%' }}>
            <button
              className="ep-btn"
              style={{
                fontSize: '16px',
                fontWeight: '800'
              }}
              onClick={attemptLogin}
            ><i className="fa fa-user-check"></i>&nbsp;&nbsp;LOGIN</button>
            <button
              className="ep-btn-orange"
              style={{
                fontSize: '16px',
                fontWeight: '800'
              }}
              onClick={() => {closeAllModals();setRegisterModal(true);}}
            ><i className="fa fa-user-plus"></i>&nbsp;&nbsp;SIGN UP</button>
          </div>
          <a href="/account-recovery" rel="noreferrer"> Forgot Password? </a>
        <UserModalFooter/>
      </div>
    </>
  }

  window.toggleLoginModal = () => {
    if (!showLoginModal) {closeAllModals(); setLoginModal(true);}
    else {closeAllModals();}
  }

  const RegisterModal = () => {
    return <>
      <div className="nav-user-modal-bg" onClick={closeAllModals}/>
      <div className="nav-user-modal" style={{paddingTop: '32px'}}>
        { showBurgerMenuIcon ?
            <></>
          :
            <div className="nav-user-modal-head">
              <i className="fa-solid fa-times nav-user-modal-close" onClick={closeAllModals}/>
            </div>
        }
        <h2>We're glad you want to join us!</h2>
        <div style={{
          padding: '0 5%',
          maxWidth: '420px',
          margin: showInviteFail ? '0 auto 5% auto' : '0 auto 10% auto'
        }}>
          However; unfortunately we are only accepting users who are invited to our beta program.
          If you think you might have been invited by another user, enter your email below.
        </div>
        { showInviteFail ?
            <div className="nav-user-modal-login-error">
              Unfortunately you haven't been invited!
            </div>
          :
            <></>
        }
        <p><img src={EmailSVG} alt="email" width="16px"/>Email</p>
        <input id="email" name="email" type="email"/>
        <div style={{ marginTop: '5%' }}>
          <button
            className="ep-btn-orange"
            style={{
              fontSize: '16px',
              fontWeight: '800'
            }}
            onClick={() => setInviteFail(true)}
          ><i className="fa fa-user-plus"></i>&nbsp;&nbsp;SIGN UP</button>
        </div>
        <UserModalFooter/>
      </div>
    </>
  }

  window.toggleRegisterModal = () => {
    if (!showRegisterModal) {closeAllModals(); setRegisterModal(true);}
    else {closeAllModals();}
  }

  return <header>
    { /* Show Mobile Navbar or Desktop Navbar */
      showBurgerMenuIcon ?
        <>
          <i
            className={
              burgerMenuOpen || showLoginModal || showRegisterModal ?
                "fa-solid fa-times mobile-nav-menu-btn"
              :
                "fa-solid fa-bars mobile-nav-menu-btn"
            }
            onClick={() => {
              if (!showLoginModal && !showRegisterModal) setBurgerMenuOpen(!burgerMenuOpen);
              else if (showRegisterModal) setRegisterModal(false);
              else setLoginModal(false);
            }}
          />
        </>
      :
        <div
          id="nav-left"
          onClick={closeAllModals}
          style={{ maxWidth: '40vw', marginLeft: '5vw' }}
        ><NavBarLinks/></div>
    }
    { /* Small Screen Nav Menu */
      burgerMenuOpen ?
        <>
          <div className="mobile-nav-menu-bg"/>
          <div className="mobile-nav-menu" onClick={() => setBurgerMenuOpen(false)}>
            <NavBarLinks/>
          </div>
        </>
      :
        <></>
    }
    { /* User Not Logged In */
      user.UUID === null ?
        <div id="nav-right">
          <button
            onClick={window.toggleLoginModal}
            style={{ border: '1px solid rgb(212, 96, 0)' }}
          > Login </button>
          <button
            onClick={window.toggleRegisterModal}
            style={{ backgroundColor: 'rgb(212, 96, 0)' }}
          > Sign Up </button>
        </div>
      :
        <div id="nav-right" className="nav-right-user">
          <Link to={`user/${user.UUID}`}>
            <p>{user.EMAIL}</p>
            <i className="fa-solid fa-user"></i>
          </Link>
        </div>
    }
    { showLoginModal ? <LoginModal/> : <></> }
    { showRegisterModal ? <RegisterModal/> : <></> }
  </header>
}


export default Navbar;
