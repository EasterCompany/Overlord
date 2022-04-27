// NODE MODULE IMPORTS
import React from 'react';
import { hydrate, render } from "react-dom";
import { BrowserRouter as Router } from "react-router-dom";

// LOCAL REQUIREMENTS
import reportWebVitals from './library/reportWebVitals';
import * as serviceWorkerRegistration from './library/serviceWorkerRegistration';

// APPLICATION IMPORTS
import './index.css';
import Routes from './routes';
import Navbar from './components/navbar/navbar';
import UserLogin from './apps/login/login';
import { userActive } from './shared/library/local/user';

// SERVER SIDE RENDERING
const _targetFunc = () => {
  if (document.getElementById("root")?.hasChildNodes())
    return hydrate
  return render
}
const targetFunc = _targetFunc()

if ( userActive() === true ) {
  // APPLICATION INDEX
  targetFunc(
    <div id="site-container">
      <Router>
        <div id="article">
          <Navbar />
          <div id="article-content">
              <Routes />
          </div>
        </div>
      </Router>
    </div>,
    document.getElementById('root')
  )
} else {
  // LOGIN CONTAINER
  targetFunc(
    <div id="site-container">
        <div id="article">
          <div id="article-content">
            <UserLogin/>
          </div>
        </div>
    </div>,
    document.getElementById('root')
  )
}

// SERVICE WORKER
serviceWorkerRegistration.unregister();

// WEB VITALS
reportWebVitals();
