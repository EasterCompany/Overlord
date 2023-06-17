// Shared library
import { oapi } from './api';


/*
  CREATE NEW USER FUNCTIONS
*/
export const create_user_from_gui = async (
  email:string, password:string, permissions:string
) => {
  const apiRequest =
    `user/create/${encodeURIComponent(email)}/${encodeURIComponent(password)}/${encodeURIComponent(permissions)}`;
  return await oapi(
    apiRequest,
    null,
    (resp: any) => null,
    (resp: any) => window.location.reload()
  )
}


/*
  LOCAL DATA (Cookies)
  contains 3 functions to:
    <cookie> get a cookie 'value by name'
    <createCookie> creates a cookie with 'name and value'
    <deleteCookie> deletes a cookie 'by name'
*/

// Get Cookie
export const cookie = (name: string) => {
  let cookieValue: any = null;

  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();

      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }

    }
  }

  return cookieValue;
};

// New Cookie
export const createCookie = (name: string, value: any) => {
  document.cookie = `${name}=${value};path=/;Secure;SameSite=None;`;
  return cookie(name);
};

// Delete Cookie
export const deleteCookie = (name: string) => {
  document.cookie = `${name}=;path=/;Secure;SameSite=None;Max-Age=-99999999;`;
  return cookie(name);
};


/*
  LOCAL USER FUNCTIONS
  set & return local cookie data
*/

// Get Local User data
export const USER = () => {

  const USR = {
    // Auth
    UUID: cookie('USR.UUID'),
    EMAIL: cookie('USR.EMAIL'),
    SESH: cookie('USR.SESH'),

    // Public
    DISPLAY_NAME: cookie('USR.DISPLAY_NAME'),
    DISPLAY_IMAGE: cookie('USR.DISPLAY_IMAGE'),

    // Private
    FIRST_NAME: cookie('USR.FIRST_NAME'),
    MIDDLE_NAMES: cookie('USR.MIDDLE_NAMES'),
    LAST_NAME: cookie('USR.LAST_NAME'),
    DOB: cookie('USR.DOB'),

    // Status
    JOINED_DATE: cookie('USR.JOINED_DATE'),
    LAST_ACTIVE: cookie('USR.LAST_ACTIVE'),
  };

  return USR;

};


// Create Local User data
export const __INIT_USER__ = (
    uuid:string, email:string, sesh:string, dob:string, name:string, image:string, fname:string, mname:string,
    lname:string, joined:string, last_active:string
  ) => {
  /*
    INIT USER <Object>
    creates local USER data with cookies stored on this device
  */
  createCookie('USR.UUID', uuid)
  createCookie('USR.EMAIL', email)
  createCookie('USR.SESH', sesh)
  createCookie('USR.DOB', dob)
  createCookie('USR.DISPLAY_NAME', name)
  createCookie('USR.DISPLAY_IMAGE', image)
  createCookie('USR.FIRST_NAME', fname)
  createCookie('USR.MIDDLE_NAME', mname)
  createCookie('USR.LAST_NAME', lname)
  createCookie('USR.JOINED_DATE', joined)
  createCookie('USR.LAST_ACTIVE', last_active)
};


// Delete all Local User data
export const deleteAllLocalCookieData = () => {
  const USR = USER()
  for(const ITEM in USR){
    deleteCookie(`USR.${ITEM}`);
  };
}


// Check if User is logged in
export const userActive = () => {
  return cookie('USR.SESH') !== null;
}


// Log Out of Current Session
export const logout = () => {
  deleteAllLocalCookieData();
  window.location.href = '';
  window.location.reload();
}


// Log in
export const login = async (email:any, password:any, BAD:any=null, OK:any=null) => {
  const encodedEmail = encodeURIComponent(email);
  await oapi(
    `user/login/${encodedEmail}`,
    password,
    (resp:any) => BAD === null ? null : BAD(resp),
    (user:any) => {
      __INIT_USER__(
        user.uuid, user.email, user.session, "", "", "", "", "",
        "", "", ""
      )
      OK === null ? window.location.reload() : OK(user)
    }
  )
}


export default USER;
export const user = USER();
