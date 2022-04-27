// Node module imports
import { Route as NewRoute, Link as NewLink, Switch } from "react-router-dom";


const scrollContentToTop = () => {
  const content = document.querySelector('#article') as HTMLElement;
  return content.scrollTop = 0;
}


export const setAppTitle = (title: string) => {
  return document.title = `${process.env.REACT_APP_NAME} | ${title}`;
}


/*
  DP (Direct Path)
  directs user to a path within the current client application
*/
export const dp = (path: string) => {
  if (process.env.REACT_APP_IS_INDEX === "true") { return '/' + path; }
  return `/${process.env.REACT_APP_ENDPOINT}/` + path;
}


/*
  ROUTE OBJECTS
  creates a new route
*/
export const Route = (props: any) => {
  if ("any" in props) { return <NewRoute path={dp(props.path)} component={props.app} />; }
  return <NewRoute path={dp(props.path)} exact component={props.app} />;
}


/*
  LINK OBJECT
  links to an existing route
*/
export const Link = (props: any) => {
  return <NewLink to={dp(props.to)} onClick={scrollContentToTop}>
    {props.name}
  </NewLink>;
}


export { Switch, NewLink }
