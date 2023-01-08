// Node module imports
import {
  Route as NewRoute,
  Link as NewLink,
  Routes as Index,
  useLocation
} from "react-router-dom";


/*
  ENDPOINT (URL for this client)
  stores the specific complete url path for this particular client
*/
const endpoint = process.env.REACT_APP_ENDPOINT === undefined ? null : process.env.REACT_APP_ENDPOINT


/*
  SCROLL CONTENT TO TOP (scrolls to the top of the page)
  will automatically scrolls any content to the top which is useful for when you
  are keeping certain elements consistent across routes, but need to reset them
*/
const scrollContentToTop = (selector:string) => {
  const content = document.querySelector(selector) as HTMLElement;
  if (content !== undefined) return content.scrollTop = 0;
  return null;
}


/*
  SET PAGE TITLE (Set HTML <Title> Content)
  overwrites the existing page title in the html for this route
*/
export const setPageTitle = (title:string) => {
  return document.title = `${title} | ${process.env.REACT_APP_NAME}`;
}


/*
  DP (Direct Path)
  directs user to a path within the current client application
*/
export const dp = (path:string) => {
  if (process.env.REACT_APP_IS_INDEX === "true") { return '/' + path; }
  return endpoint === null ? '/' + path : `/${process.env.REACT_APP_ENDPOINT}/` + path;
}


/*
  GOTO (Additional Path)
  sends the user to a valid path within the scope of this client
*/
const goto = (path:string) => {
  let URL = window.location.pathname;
  if (!URL.endsWith('/')) { URL += '/' }
  window.location.href = URL + path;
}


/*
  ROUTE OBJECT (React-Router-Dom Wrapper)
  creates a new route
*/
export const Route = (props: any) => <NewRoute path={dp(props.path)} element={
  props.app === undefined ? <props.page/> : <props.app/>
}/>

/*
  LINK OBJECT (Route Navigation Button)
  links to an existing route
*/
export const Link = ({ to, name, children } : any) => {
  return <NewLink to={dp(to)} onClick={() => scrollContentToTop('#site-container')}>
    {name !== undefined ? name : ""}
    {children !== undefined ? children : <></>}
  </NewLink>;
}


export { Index, NewLink, useLocation }
export default goto;
