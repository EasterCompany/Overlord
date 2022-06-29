// Component imports
import './navbar.css';
import settingImg from '../../shared/assets/icons/settings.svg';
import { Link, dp } from "../../shared/components/routes/routes";


const navbarClick = (forceClose=false) => {
  // Fetch objects
  const btn = document.querySelector('#navbar-menu-button') as HTMLElement;
  const menu = document.querySelector('#navbar') as HTMLElement;

  // Toggle menu & button
  if (btn?.className === 'navbar-menu-open' || forceClose) {
    btn.className = 'navbar-menu-closed';
    menu.className = 'navbar-closed';
    return;
  }

  // Default menu & button
  btn.className = 'navbar-menu-open';
  menu.className = 'navbar-open';
}


const Navbar = () => <div id="nav-header">
  <div id="header"
    style={{backgroundImage: `url("${settingImg}")`}}
    onClick={() => window.location.href = dp('')}
  />

  <nav
    id="navbar"
    className="navbar-closed"
    onClick={() => navbarClick(true)}
  >
    {/* NAVBAR BUTTONS */}
    <Link to="users" name="Users" />
    <Link to="posts" name="Posts" />
    <Link to="jobs" name="Jobs" />
    <Link to="gallery" name="Gallery" />
  </nav>

  {/* OPEN/CLOSE NAVIGATION (MOBILE) */}
  <div
    id="navbar-menu-button"
    className="navbar-menu-closed"
    onClick={() => navbarClick(false)}
  />

</div>


export default Navbar;
