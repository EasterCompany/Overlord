// Local Apps ---------------------
// Default Home Page
import Home from './apps/home/home';
// User Pages
import Users from './apps/users/list';
import UsersEdit from './apps/users/edit';
// Jobs Pages
import JobsList from './apps/jobs/list';
import JobsEdit from './apps/jobs/edit';
// Posts Pages
import PostsList from './apps/posts/list';
import PostsEditView from './apps/posts/edit';
// Locals Apps error imports ------
import PageNotFoundError from './apps/404/404';
// Local imports ------------------
import { Route, Switch } from './shared/components/routes/routes';


// App routes
const Routes = () => {
  return <Switch>

    { // [HOME] Default Page
      Route({path: '', app: Home})
    }
    {
      Route({path: 'e_panel', app: Home})
    }


    { // [USER] List Page
      Route({
        path: 'users',
        app: Users
      })}
    { //        View & Edit Page
      Route({
        path: 'users/:uid',
        app: UsersEdit
    })}

    { // [POST]  List Page
      Route({
        path: 'posts',
        app: PostsList
    })}
    { //        View & Edit Page
      Route({
        path: 'posts/:uid',
        app: PostsEditView
    })}


    { // [JOB]  List Page
      Route({
        path: 'jobs',
        app: JobsList
    })}
    { //        View & Edit Page
      Route({
        path: 'jobs/:uid',
        app: JobsEdit
    })}


    { // [404]  Page not found
      Route({
        path: '*',
        any: true,
        app: PageNotFoundError
    })}

  </Switch>
}

export default Routes;
