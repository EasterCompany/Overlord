// Local imports
import '../global.css';
// React imports
import { useState, useEffect } from 'react';
// Shared components
import Table from '../../shared/components/tables/table';
// Shared library
import { create_user_from_gui } from '../../shared/library/local/user';
import api, { serverAPI } from '../../shared/library/server/api';

const tableTitle = "Users";
const docTitle = `[E PANEL] ${tableTitle}`;
const apiURL = serverAPI + "user/";


/*
  CREATE NEW USER VIEW
  contains a modal with a create new user form
*/
const CreateView = (props: any) => <div className="full-modal">

  <div className="modal-form">
    <h1 className="tableHeader"> NEW USER </h1>
      <div className="table-inputs">

        <label htmlFor="email"> Email </label>
        <input className="table-input" type="text" id="email" name="email" required/>

        <label htmlFor="_pass"> Password </label>
        <input className="table-input" type="text" id="_pass" name="_pass" required/>

        <label htmlFor="perms"> Permissions </label>
        <select className="table-input" id="perms" name="perms" required>
          <option value="1"> User </option>
          <option value="2"> Staff </option>
          <option value="3"> Management </option>
          <option value="9"> Software Engineer </option>
        </select>

      </div>
  </div>

  <div className="flex-center">
    <button onClick={() => props.close()}> Cancel </button>
    <button type="submit" onClick={async () => {
      const email_el = document.getElementById("email") as HTMLInputElement;
      const password = document.getElementById("_pass") as HTMLInputElement;
      const perms_el = document.getElementById("perms") as HTMLInputElement;

      if (email_el.value === '') email_el.style.backgroundColor = "red";
      if (password.value === '') email_el.style.backgroundColor = "red";

      return create_user_from_gui(
        email_el.value,
        password.value,
        perms_el.value,
      );

    }}> Submit </button>
  </div>

</div>


/*
  USERS TABLE
  contains a generic table which outputs local database user data
*/
const Users = () => {
  const [head, setHead] = useState([]);
  const [body, setBody] = useState([]);

  useEffect( () => {

    const updateTable = () => {
      api(
        "user/view",
        (data: string) => alert(`[ERROR Updating ${tableTitle} Tables] ${data}`),
        (data: any) => {
          if (head !== data.head) setHead(data.head)
          if (body !== data.body) setBody(data.body)
        }
      )
    }

    if (document.title !== docTitle) {
      document.title = docTitle;
      updateTable();
    }

  })

  return <Table
    /* BASICS */
    name={"USERS"}
    previewSize={10}

    /* TABLE DATA */
    headers={head}
    data={body}

    /* API PATHS */
    view={apiURL + 'get'}
    create={apiURL + 'create'}
    delete={'user/delete'}

    /* ACTION VIEWS */
    CreateView={CreateView}
  />
}


export default Users;
