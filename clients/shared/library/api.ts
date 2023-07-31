// Use AsyncStorage for native cookies
import AsyncStorage from '@react-native-async-storage/async-storage';

// Shortcuts
export const isNative = typeof window.location === 'undefined' || typeof document === 'undefined';
export const isDev = process.env.REACT_APP_ENV === 'Dev';
export const isPrd = process.env.REACT_APP_ENV === 'Prd';
export const mock = isNative ? (_url:string) => {
  return isDev ?
    _url.replace(_url.split('/')[2], `${process.env.API_DOMAIN}:8000`).replace('https://', 'http://') : _url
} : (_url:string) => {
  return isDev ?
    _url.replace(_url.split('/')[2], '0.0.0.0:8000').replace('https://', 'http://') : _url
};
if (isNative) {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const document = { cookie: {} };
};


// Defines the routing for this client & server environment
export const getEndpoints = isNative ? () => {
  const client_endpoint = process.env.REACT_APP_ENDPOINT === `` ? `/` : `/${process.env.REACT_APP_ENDPOINT}/`
  return {
    client: isDev ? '/' : client_endpoint,
    server: `${process.env.API_DOMAIN}/`,
    api: `${process.env.API_DOMAIN}/api/${process.env.REACT_APP_NAME}`
  };
} : () => {
  if (window.location.host.endsWith(':3000')) {
    return {
      client: 'http://localhost:3000/',
      server: 'http://localhost:3000/',
      api: `http://localhost:3000/api/`
    };
  } else if (window.location.host.startsWith('localhost')) {
    const client_endpoint =
      process.env.REACT_APP_NAME === '' ?
        `http://localhost:8000/` :
        `http://localhost:8000/${process.env.REACT_APP_NAME}/`
    return {
      client: client_endpoint,
      server: `http://localhost:8000/`,
      api: `http://localhost:8000/${process.env.REACT_APP_API}`
    };
  } else if (window.location.host.startsWith('0.0.0.0')) {
    return {
      client: process.env.REACT_APP_NAME === '' ?
        `http://0.0.0.0:8000/` :
        `http://0.0.0.0:8000/${process.env.REACT_APP_NAME}/`,
      server: `http://0.0.0.0:8000/`,
      api: `http://0.0.0.0:8000/${process.env.REACT_APP_API}`
    };
  } else if (window.location.host.startsWith('127.0.0.1')) {
    return {
      client: process.env.REACT_APP_NAME === '' ?
        `http://127.0.0.1:8000/` :
        `http://127.0.0.1:8000/${process.env.REACT_APP_NAME}/`,
      server: `http://127.0.0.1:8000/`,
      api: `http://127.0.0.1:8000/${process.env.REACT_APP_API}`
    }
  } else if (window.location.host.startsWith('192.168.')) {
    const client_endpoint =
      process.env.REACT_APP_NAME === '' ?
        `http://${window.location.host.split(':')[0]}:8000/` :
        `http://${window.location.host.split(':')[0]}:8000/${process.env.REACT_APP_NAME}/`
    return {
      client: client_endpoint,
      server: `http://${window.location.host.split(':')[0]}:8000/`,
      api: `http://${window.location.host.split(':')[0]}:8000/${process.env.REACT_APP_API}`
    };
  } else {
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
};


// Request data from the Client Specific API
export const api = async (API: string, BAD: any = null, OK: any = null) => {
  USER().then(async (user:any) => {
    try {
      const response = await fetch(`${clientAPI}${API}`, {
        method: 'POST',
        headers: {
          'Authorization': `Basic ${user.uuid} ${user.session}`,
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
      return BAD("Unexpected Server Error")
    };
  });
};


// POST data to the client specific API
export const POST = async (API: string, BAD: any = null, OK: any = null, _POST: any,) => {
  USER().then(async (user:any) => {
    await fetch(`${clientAPI}${API}`, {
      method: 'POST',
      headers: new Headers({
        'Authorization': `Basic ${user.uuid} ${user.session}`,
        'Content-Type': 'application/json'
      }),
      body: JSON.stringify(_POST),
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
  });
};


// Request data from an External API
export const xapi = async (
  API: string = "",
  CALLBACK: any = null,
  DATA: any = "",
  AUTH: any = "",
  MOCK: boolean = true
) => {
  try {
    await fetch(MOCK ? mock(API) : API, {
      method: 'POST',
      headers: new Headers({
        'Authorization': `${AUTH}`,
        'Content-Type': DATA === null ? 'application/x-www-form-urlencoded' : 'application/json'
      }),
      body: DATA,
    })
    .then(resp => resp.json())
    .then(respJson => CALLBACK(respJson))
  } catch (error) {
    console.log(`Error @ ${API}`);
    console.log(error);
    return
  }
};


// Post/Request data to/from an Overlord Built-in API
export const oapi = async (API: string, BAD: any = null, OK: any = null, DATA: any = null) => {
  USER().then((user:any) => {
    try {
      fetch(`${serverAdr}api/o-core/${API}`, {
        method: 'POST',
        headers: new Headers({
            'Authorization': `Basic ${user.uuid} ${user.session}`,
            'Content-Type': DATA === null ? 'application/x-www-form-urlencoded' : 'application/json'
        }),
        body: JSON.stringify(DATA)
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
    } catch (error) {
      console.log(`Error @ ${API}`);
      console.log(error);
      return BAD("Unexpected Server Error")
    }
  });
};


// Login using the built-in Overlord user model
export const login = (BAD:any, OK:any, email:string, password:string, ) => {
  oapi(
    'user/login',
    (resp:any) => BAD(resp),
    (resp:any) => __INIT_USER__(resp).then(() => OK(resp)),
    {
      email: email,
      password: password
    }
  );
};


// Log Out of Current Session
export const logout = async (noRefresh:boolean=false) => {
  deleteAllCookies().then(() => {
    if (!isNative && !noRefresh) {
      window.location.href = '';
      window.location.reload();
    }
  });
};


// Create local user data
export const __INIT_USER__ = async (resp:any) => {
  // Auth
  await createCookie('USR.uuid', resp.uuid);
  await createCookie('USR.email', resp.email);
  await createCookie('USR.session', resp.session);
  await createCookie('USR.groups', JSON.stringify(resp.groups));
  await createCookie('USR.permissions', resp.permissions);
  // Details
  await createCookie('USR.firstName', resp.firstName);
  await createCookie('USR.middleNames', resp.middleNames);
  await createCookie('USR.lastName', resp.lastName);
  await createCookie('USR.displayName', resp.displayName);
  await createCookie('USR.displayImage', resp.displayImage);
  await createCookie('USR.dateOfBirth', resp.dateOfBirth);
  // Status
  await createCookie('USR.dateJoined', resp.dateJoined);
  await createCookie('USR.lastActive', resp.lastActive);
};


// Get local user data
export const USER = async () => {
  const userData = {
    // Auth
    uuid: await cookie('USR.uuid'),
    email: await cookie('USR.email'),
    session: await cookie('USR.session'),
    groups: await cookie('USR.groups'),
    permissions: await cookie('USR.permissions'),
    // Details
    displayName: await cookie('USR.displayName'),
    displayImage: process.env.API_DOMAIN ?
      process.env.API_DOMAIN + await cookie('USR.displayImage') :
      await cookie('USR.displayImage'),
    firstName: await cookie('USR.firstName'),
    middleNames: await cookie('USR.middleNames'),
    lastName: await cookie('USR.lastName'),
    dateOfBirth: await cookie('USR.dateOfBirth'),
    // Status
    dateJoined: await cookie('USR.dateJoined'),
    lastActive: await cookie('USR.lastActive'),
  };

  // middlesNames is never undefined
  if (userData.middleNames === undefined) userData.middleNames = ''

  // Parse USER.groups JSON
  userData.groups === undefined || userData.groups === null ? userData.groups = {} : JSON.parse(userData.groups)

  return userData;
};


// Read AsyncStorage key value
const nativeCookie = async (key:string) => {
  try {
    const cookieValue = await AsyncStorage.getItem(key).then((value:any) => value);
    return cookieValue
  } catch (e) {
    console.log(`Database Error while reading key(${key}): ${e}`);
    return null
  }
};


// Read cookie data
export const cookie = async (key: string) => {
  let cookieValue: any = null;
  if (isNative) {
    cookieValue = await nativeCookie(key);
  } else if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, key.length + 1) === (key + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(key.length + 1));
        break;
      }
    }
  }
  return cookieValue === "" || cookieValue === null ? undefined : cookieValue;
};


// Create AsyncStorage key value
const createNativeCookie = async (key:string, value:string) => {
  if (!isNative) return;
  try {
    await AsyncStorage.setItem(key, `${value}`);
  } catch (e) {
    console.log(`Database Error while creating key(${key}): ${e}`);
  }
};


// Create new cookie
export const createCookie = async (key: string, value: any) => {
  if (isNative) {
    await createNativeCookie(key, value);
  } else {
    document.cookie = `${key}=${value};path=/;Secure;SameSite=None;`;
  }
};


// Remove AsyncStorage key value
const deleteNativeCookie = async (key:string) => {
  try {
    await AsyncStorage.removeItem(key);
  } catch (e) {
    console.log(`Database Error while removing key(${key}): ${e}`);
  }
};


// Delete cookie
export const deleteCookie = async (key: string) => {
  if (isNative) {
    await deleteNativeCookie(key);
  } else {
    document.cookie = `${key}=;path=/;Secure;SameSite=None;Max-Age=0;expires=` + new Date(0).toUTCString();
  }
};


// Delete all Local User data
export const deleteAllCookies = async () => {
  if (isNative) {
    const cookies = await AsyncStorage.getAllKeys();
    await AsyncStorage.multiRemove(cookies);
  } else {
    USER().then((userCookies) => Object.keys(userCookies).map((cookie) => {
      return deleteCookie(`USR.${cookie}`);
    }));
  };
};


// Check if User is logged in
export const isLoggedIn = (callback:any) => {
  return cookie('USR.session').then((session) => callback(session !== undefined))
};


// Export the client->server environment
export default api;
export const endPoints = getEndpoints();
export const clientAdr = endPoints.client;
export const serverAdr = endPoints.server;
export const clientAPI = endPoints.api;
