// Overlord library
import { USER } from './user';

// Shortcuts
export const isDev = window.location.toString().startsWith("http://localhost:8");
export const isPrd = !isDev;
export const mock = (_url:string) => isDev ?
  _url.replace(_url.split('/')[2], 'localhost:8000').replace('https://', 'http://') : _url

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

  // Localhost Django Server
  else if (window.location.host.startsWith('localhost')) {
    const client_endpoint =
      process.env.REACT_APP_NAME === '' ?
        `http://localhost:8000/` :
        `http://localhost:8000/${process.env.REACT_APP_NAME}/`
    return {
      client: client_endpoint,
      server: `http://localhost:8000/`,
      api: `http://localhost:8000/${process.env.REACT_APP_API}`
    };
  }

  // 0.0.0.0 Default Django Server
  else if (window.location.host.startsWith('0.0.0.0')) {
    const client_endpoint =
      process.env.REACT_APP_NAME === '' ?
        `http://0.0.0.0:8000/` :
        `http://0.0.0.0:8000/${process.env.REACT_APP_NAME}/`
    return {
      client: client_endpoint,
      server: `http://0.0.0.0:8000/`,
      api: `http://0.0.0.0:8000/${process.env.REACT_APP_API}`
    };
  }

  // Parent 127..:8000 & 127...:81XX Django Server
  else if (window.location.host.startsWith('http://127.0.0.1:8')) {
    if (window.location.host === 'http://127.0.0.1:8000') {
      return {
        client: process.env.REACT_APP_NAME === '' ?
          `http://127.0.0.1:8000/` :
          `http://127.0.0.1:8000/${process.env.REACT_APP_NAME}/`,
        server: `http://127.0.0.1:8000/`,
        api: `http://127.0.0.1:8000/${process.env.REACT_APP_API}`
      }
    }
    return {
      client: window.location.host,
      server: `http://127.0.0.1:8000/`,
      api: `http://127.0.0.1:8000/${process.env.REACT_APP_API}`
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
      api: `http://${window.location.host.split(':')[0]}:8000/${process.env.REACT_APP_API}`
    };
  }

  // World Wide Web
  else {
    const client_endpoint =
      process.env.REACT_APP_NAME === '' ?
        `https://${window.location.host}/` :
        `https://${window.location.host}/${process.env.REACT_APP_NAME}/`
    return {
      client: client_endpoint,
      server: `https://${window.location.host}/`,
      api: `https://${window.location.host}/${process.env.REACT_APP_API}`
    };
  }
}


/*
  SERVER API FUNCTIONS
  these may require certain access & permissions parameters
*/

// Request data from the API
export const api = async (API: string, BAD: any = null, OK: any = null) => {
  const user = USER();
  const _auth = `${user.UUID} ${user.SESH}`;

  try {
    const response = await fetch(serverAPI + API, {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${_auth}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const respJson = await response.json();
    const respStatus = respJson['status'];
    const respData = respJson['data'];

    if (respStatus === 'OK') {
      return OK !== null ? OK(respData) : respData;
    } else if (respStatus === 'BAD') {
      return BAD !== null ? BAD(respData) : respData;
    }

  } catch (error) {
    console.log(`Error @ ${API}`);
    console.log(error);
    return BAD({})
  }

};

// Request data from the API
export const POST = async (API: string, _POST: any, BAD: any = null, OK: any = null) => {
  const user = USER();
  const _auth = `${user.UUID} ${user.SESH}`;

  await fetch(serverAPI + API, {
    method: 'POST',
    headers: new Headers({
      'Authorization': `Basic ${_auth}`,
      'Content-Type': 'application/json'
    }),
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


// Request data from an External API
export const xapi = async (
  API: string = "",
  CALLBACK: any = null,
  DATA: any = "",
  AUTH: any = "",
  MOCK: boolean = true
) => {
  await fetch(MOCK ? mock(API) : API, {
    method: 'POST',
    headers: new Headers({
      'Authorization': `Basic ${AUTH}`,
      'Content-Type': DATA === null ? 'application/x-www-form-urlencoded' : 'application/json'
    }),
    body: DATA,
  })
  .then(resp => resp.json())
  .then(respJson => CALLBACK(respJson))
}


// Request data from a Base Overlord API
export const oapi = async (API: string, DATA: any = null, BAD: any = null, OK: any = null) => {
  const user = USER();
  const _auth = `${user.UUID} ${user.SESH}`;

  await fetch(`${serverAdr}api/${API}`, {
    method: 'POST',
    headers: new Headers({
        'Authorization': `Basic ${_auth}`,
        'Content-Type': DATA === null ? 'application/x-www-form-urlencoded' : 'application/json'
    }),
    body: DATA
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

// Core API Library
export default api;
export const endPoints = getEndpoints();
export const clientAdr = endPoints.client;
export const serverAdr = endPoints.server;
export const serverAPI = endPoints.api;
