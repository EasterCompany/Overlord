import {
  cookie, logout as logoutLocally, USER
} from '../local/user';


/*
  GLOBAL ENVIRONMENT SETUP
  defines the routing for this Clients Environment
*/
export const getEndpoints = () => {

  // Standalone Local Django Server
  if (window.location.host.endsWith(':3000')) {
    return {
      client: 'http://localhost:3000/',
      server: 'http://localhost:3000/',
      api: `http://localhost:3000/api/`
    };
  }

  // Parent Local Django Server
  else if (window.location.host.startsWith('localhost')) {
    const client_endpoint =
      process.env.REACT_APP_NAME === '' ?
        `http://localhost:8000/` :
        `http://localhost:8000/${process.env.REACT_APP_NAME}/`
    return {
      client: client_endpoint,
      server: `http://localhost:8000/`,
      api: `http://localhost:8000/api/`
    };
  }

  // Parent 127..:8000 & 127...:81XX Django Server
  else if (window.location.host.startsWith('http://127.0.0.1:8')) {
    if (window.location.host === 'http://127.0.0.1:8000') {
      return {
        client: process.env.REACT_APP_NAME === '' ?
          `http://127.0.0.1:8000/` :
          `http://127.0.0.1:8000/${process.env.REACT_APP_NAME}/`,
        server: `http://127.0.0.1:8000/admin`,
        api: `http://127.0.0.1:8000/api`
      }
    }
    return {
      client: window.location.host,
      server: `http://127.0.0.1:8000/admin`,
      api: `http://127.0.0.1:8000/api`
    }
  }

  // Local Network React App (Mobile Testing)
  else if (window.location.host.startsWith('192.168.')) {
    const client_endpoint =
      process.env.REACT_APP_NAME === '' ?
        `http://${window.location.host.split(':')[0]}:8000/` :
        `http://${window.location.host.split(':')[0]}:8000/${process.env.REACT_APP_NAME}/`
    return {
      client: client_endpoint,
      server: `http://${window.location.host.split(':')[0]}:8000/`,
      api: `http://${window.location.host.split(':')[0]}:8000/${process.env.REACT_APP_API}/`
    };
  }

  // World Wide Web
  else {
    const client_endpoint =
      process.env.REACT_APP_NAME === '' ?
        `http://${window.location.host}/` :
        `http://${window.location.host}/${process.env.REACT_APP_NAME}/`
    return {
      client: client_endpoint,
      server: `https://${window.location.host}/`,
      api: `https://${window.location.host}/${process.env.REACT_APP_API}/`
    };
  }
}


// Encode list to uri
const APIPath = (paths:any) => {
  let pathString = "api";

  paths.forEach( (path:string) => {
    pathString += "/" + encodeURIComponent(path);
  })

  return pathString;
}


/*
  SERVER API FUNCTIONS
  these may require certain access & permissions parameters
*/

// Request data from the API
export const api = async (API: string, BAD: any = null, OK: any = null) => {
  const user = USER();
  const _auth = user.SESH;

  await fetch(serverAPI + API, {
    method: 'post',
    headers: new Headers({
        'Authorization': `Basic ${_auth}`,
        'Content-Type': 'application/x-www-form-urlencoded'
    })
  })
  .then(resp => resp.json())
  .then(respJson => {

    const respStatus = respJson['status'];
    const respData = respJson['data'];

    // OK API RESULT HANDLER
    if (respStatus === 'OK') {
      try { return OK !== null ? OK(respData) : respData }
      catch (error) {
        console.log(`OK Callback Error @ ${API}`)
        console.log({status:respStatus, data:respData, error:error})
      }
    }

    // BAD API RESULT HANDLER
    else if (respStatus === 'BAD') {
      try{ return BAD !== null ? BAD(respData) : respData }
      catch (error) {
        console.log(`BAD Callback Error @ ${API}`)
        console.log({status:respStatus, data:respData, error:error})
      }
    }
  })
}

// Request data from the API
export const POST = async (API: string, _POST: any, BAD: any = null, OK: any = null) => {
  const user = USER();
  const _auth = user.SESH; // user auth is currently not taken any further

  await fetch(serverAPI + API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: _POST,
  })
  .then(resp => resp.json())
  .then(respJson => {

    const respStatus = respJson['status'];
    const respData = respJson['data'];

    // OK API RESULT HANDLER
    if (respStatus === 'OK') {
      try { return OK !== null ? OK(respData) : respData }
      catch (error) {
        console.log(`OK Callback Error @ ${API}`)
        console.log({status:respStatus, data:respData, error:error})
      }
    }

    // BAD API RESULT HANDLER
    else if (respStatus === 'BAD') {
      try{ return BAD !== null ? BAD(respData) : respData }
      catch (error) {
        console.log(`BAD Callback Error @ ${API}`)
        console.log({status:respStatus, data:respData, error:error})
      }
    }
  })
}


/*
  GLOBAL ENVIRONMENT
  contains the state of the API->Client relationship.
*/
export default api;
export const endPoints = getEndpoints();
export const clientAdr = endPoints.client;
export const serverAdr = endPoints.server;
export const serverAPI = endPoints.api;
