// Local imports
import '../edit.css';
import '../global.css';
// React imports
import { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
// Shared library
import api, { clientAdr, POST } from '../../shared/library/server/api';
// Shared components
import Table from '../../shared/components/tables/table';
import ConfirmationModal from '../../shared/components/modals/confirmation';

const tableTitle = "Edit Job";
const docTitle = `[E PANEL] ${tableTitle}`;
const apiURL = "job/";

let initialContent = ``;
let applicationsBody: any = [];

/*
  E DOC temporary functions
  remove these when you remove the built-in e doc editor
*/
const updateChanges = () => {
  const content = document.getElementById("e-doc-content") as HTMLElement;
  const editor = document.getElementById("e-doc-edit-content") as HTMLInputElement;
  content.innerHTML = editor.value;
}


const removeChanges = () => {
  const content = document.getElementById("e-doc-content") as HTMLElement;
  const editor = document.getElementById("e-doc-edit-content") as HTMLInputElement;
  content.innerHTML = '';
  editor.value = '';
}


/*
  JOBS VIEW & EDIT
  display all data on a job entry with options to edit certain values
*/
const JobsEdit = () => {
  const [deleteView, setDeleteView] = useState(false);
  const [htmlContent, setHtmlContent] = useState("");
  const [appsContent, setAppsContent] = useState([]);
  const URL:any = useParams()

  const editView = (open:boolean, save:boolean) => {
    const jobTitle = document.getElementById("job_title") as HTMLElement;
    const jobTitleInput = document.getElementById("job_title_input") as HTMLInputElement;
    jobTitle.style.display = open ? "none" : "block";
    jobTitleInput.style.display = open ? "block" : "none";

    const jobClient = document.getElementById("job_client") as HTMLElement;
    const jobClientInput = document.getElementById("job_client_input") as HTMLInputElement;
    jobClient.style.display = open ? "none" : "block";
    jobClientInput.style.display = open ? "block" : "none";

    const jobMinSalary = document.getElementById("job_min_salary") as HTMLElement;
    const jobMinSalaryInput = document.getElementById("job_min_salary_input") as HTMLInputElement;
    jobMinSalary.style.display = open ? "none" : "block";
    jobMinSalaryInput.style.display = open ? "block" : "none";

    const jobMaxSalary = document.getElementById("job_max_salary") as HTMLElement;
    const jobMaxSalaryInput = document.getElementById("job_max_salary_input") as HTMLInputElement;
    jobMaxSalary.style.display = open ? "none" : "block";
    jobMaxSalaryInput.style.display = open ? "block" : "none";

    const jobLocation = document.getElementById("job_location") as HTMLElement;
    const jobLocationInput = document.getElementById("job_location_input") as HTMLInputElement;
    jobLocation.style.display = open ? "none" : "block";
    jobLocationInput.style.display = open ? "block" : "none";

    const edit_btn = document.getElementById("edit_btn") as HTMLElement;
    const delete_btn = document.getElementById("delete_btn") as HTMLElement;
    edit_btn.style.display = open ? "none" : "flex";
    delete_btn.style.display = open ? "none" : "flex";

    const save_edit_btn = document.getElementById("save_edit_btn") as HTMLElement;
    const close_edit_btn = document.getElementById("cancel_edit_btn") as HTMLElement;
    save_edit_btn.style.display = open ? "flex" : "none";
    close_edit_btn.style.display = open ? "flex" : "none";

    if (save) {
      api(
        apiURL +
        `update/${encodeURIComponent(URL.uid)}/${encodeURIComponent(jobTitleInput.value)}/` +
        `${encodeURIComponent(jobClientInput.value)}/${encodeURIComponent(jobLocationInput.value)}/` +
        `${encodeURIComponent(jobMinSalaryInput.value)}/${encodeURIComponent(jobMaxSalaryInput.value)}`,

        (resp: any) => null,
        (resp: any) => {
          jobTitle.innerText = jobTitleInput.value;
          jobClient.innerText = jobClientInput.value;
          jobMinSalary.innerText = jobMinSalaryInput.value;
          jobMaxSalary.innerText = jobMaxSalaryInput.value;
          jobLocation.innerText = jobLocationInput.value;
        }
      );
    }
  }

  useEffect( () => {
    const fetchJobData = () => {

      api(
        apiURL + `get/${URL.uid}`,
        (resp: any) => alert(`[ERROR acquiring job entry for ${URL.uid}] ${resp}`),
        (resp: any) => {

          const jobTitle = document.getElementById("job_title") as HTMLElement;
          const jobTitleInput = document.getElementById("job_title_input") as HTMLInputElement;
          jobTitle.innerHTML = resp.title;
          jobTitleInput.value = resp.title; jobTitleInput.style.display = "none";

          const jobClient = document.getElementById("job_client") as HTMLElement;
          const jobClientInput = document.getElementById("job_client_input") as HTMLInputElement;
          jobClient.innerHTML = resp.client;
          jobClientInput.value = resp.client; jobClientInput.style.display = "none";

          const jobMinSalary = document.getElementById("job_min_salary") as HTMLElement;
          const jobMinSalaryInput = document.getElementById("job_min_salary_input") as HTMLInputElement;
          jobMinSalary.innerHTML = resp.min_salary;
          jobMinSalaryInput.value = resp.min_salary; jobMinSalaryInput.style.display = "none";

          const jobMaxSalary = document.getElementById("job_max_salary") as HTMLElement;
          const jobMaxSalaryInput = document.getElementById("job_max_salary_input") as HTMLInputElement;
          jobMaxSalary.innerHTML = resp.max_salary;
          jobMaxSalaryInput.value = resp.max_salary; jobMaxSalaryInput.style.display = "none";

          const jobLocation = document.getElementById("job_location") as HTMLElement;
          const jobLocationInput = document.getElementById("job_location_input") as HTMLInputElement;
          jobLocation.innerHTML = resp.location;
          jobLocationInput.value = resp.location; jobLocationInput.style.display = "none";

          const jobCreated = document.getElementById("job_created") as HTMLElement;
          jobCreated.innerHTML = resp.timestamp.split(' ')[0];

          const contentBox = document.getElementById("e-doc-content") as HTMLElement;
          const editBox = document.getElementById("e-doc-edit-content") as HTMLInputElement;
          contentBox.innerHTML = resp.info;
          editBox.innerHTML = resp.info;
          initialContent = resp.info;

          // Create Applicants Table Body
          for(const application in resp.applications){
            applicationsBody.push([
              "No UUID",
              application,
              resp.applications[application].fname,
              resp.applications[application].lname,
              resp.applications[application].tel
            ]);
          }
          setAppsContent(applicationsBody);

        }
      )
    }

    if (document.title !== docTitle) {
      document.title = docTitle;
      fetchJobData();
    }

  })

  if (deleteView) {
    const modal = {
      header: `DELETE [ JOBS ] POST`,
      message: `delete ${URL.uid}`,
      accept: () => {
        api(
          `job/delete/${encodeURIComponent(URL.uid)}`,
          (resp: any) => null,
          (resp: any) => window.location.href = clientAdr + 'jobs'
        );
      },
      cancel: () => window.location.reload()
    }

    return <ConfirmationModal modal={modal} />
  }

  return <>
    <div id="edit-panels-top-row">

      <div id="edit-panel-left">
        <h2 id="job_title">&nbsp;</h2>
        <input id="job_title_input" placeholder="Job Title" />

        <h3 id="job_client">&nbsp;</h3>
        <input id="job_client_input" placeholder="Client" />

        <hr style={{ width: '100%' }}/>
        <div style={{ display: 'flex' }}>
          <h4 style={{ margin: '1.25vh 0 1.25vh 0' }}>£ &nbsp;</h4>

          <h4 id="job_min_salary" style={{ margin: '1.25vh 0 1.25vh 0' }}>&nbsp;</h4>
          <input id="job_min_salary_input" type="number" style={{ width: '50%' }} placeholder="min salary" />

          <h4 style={{ margin: '1.25vh 0 1.25vh 0', maxHeight: '16px', padding: '0 0 0 0' }}> &nbsp; to &nbsp; </h4>

          <h4 id="job_max_salary" style={{ margin: '1.25vh 0 1.25vh 0' }}>&nbsp;</h4>
          <input id="job_max_salary_input" type="number" style={{ width: '50%' }} placeholder="max salary" />

          <h4 style={{ margin: '1.25vh 0 1.25vh 0' }}>&nbsp; K</h4>
        </div>

        <h4 id="job_location">&nbsp;</h4>
        <input id="job_location_input" placeholder="Job Location" />

        <h4 id="job_created">&nbsp;</h4>
      </div>

      <div id="edit-panel-right">

        <button
          id="edit_btn"
          onClick={() => editView(true, false)}
          style={{ display: 'flex', justifyContent: 'center' }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18px" height="18px"
            style={{ margin: '2px' }}
            viewBox="0 0 24 24" fill="white"
          >
            <path d="
                M9 19h-4v-2h4v2zm2.946-4.036l3.107 3.105-4.112.931 1.005-4.036zm12.054-5.839l-7.898 7.996-3.202-3.202
                7.898-7.995 3.202 3.201zm-6 8.92v3.955h-16v-20h7.362c4.156 0 2.638 6 2.638 6s2.313-.635
                4.067-.133l1.952-1.976c-2.214-2.807-5.762-5.891-7.83-5.891h-10.189v24h20v-7.98l-2 2.025z
            "/>
          </svg>
          <h4 style={{ margin: "1px 0 0 12px", padding: "0 0 0 0" }}> EDIT </h4>
        </button>

        <button
          id="delete_btn"
          onClick={() => setDeleteView(!deleteView)}
          style={{ display: 'flex', justifyContent: 'center' }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18px" height="18px"
            style={{ margin: '2px' }}
            viewBox="0 0 24 24" fill="white"
          >
            <path d="
              M3 6v18h18v-18h-18zm5 14c0 .552-.448 1-1 1s-1-.448-1-1v-10c0-.552.448-1 1-1s1 .448 1 1v10zm5 0c0
              .552-.448 1-1 1s-1-.448-1-1v-10c0-.552.448-1 1-1s1 .448 1 1v10zm5 0c0 .552-.448
              1-1 1s-1-.448-1-1v-10c0-.552.448-1 1-1s1 .448 1 1v10zm4-18v2h-20v-2h5.711c.9 0 1.631-1.099 1.631-2h5.315c0
              .901.73 2 1.631 2h5.712z
            "/>
          </svg>
          <h4 style={{ margin: "1px 0 0 12px", padding: "0 0 0 0" }}> DELETE </h4>
        </button>

        <button
          id="save_edit_btn"
          onClick={() => editView(false, true)}
          style={{ display: 'none', justifyContent: 'center', backgroundColor: '#22923e' }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18px" height="18px"
            style={{ margin: '2px' }}
            viewBox="0 0 24 24" fill="white"
          >
            <path d="M15.003 3h2.997v5h-2.997v-5zm8.997 1v20h-24v-24h20l4 4zm-19 5h14v-7h-14v7zm16 4h-18v9h18v-9z"/>
          </svg>
          <h4 style={{ margin: "1px 0 0 12px", padding: "0 0 0 0" }}> SAVE </h4>
        </button>

        <button
          id="cancel_edit_btn"
          onClick={() => editView(false, false)}
          style={{ display: 'none', justifyContent: 'center' }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18px" height="18px"
            style={{ margin: '2px' }}
            viewBox="0 0 24 24" fill="white"
          >
            <path d="
              M24 20.188l-8.315-8.209 8.2-8.282-3.697-3.697-8.212 8.318-8.31-8.203-3.666 3.666 8.321 8.24-8.206
              8.313 3.666 3.666 8.237-8.318 8.285 8.203z
            "/>
          </svg>
          <h4 style={{ margin: "1px 0 0 12px", padding: "0 0 0 0" }}> CANCEL </h4>
        </button>
      </div>
    </div>


    <h3> User Applications </h3>
    <Table
      /* BASICS */
      name={"Job Applications"}
      previewSize={5}
      /* TABLE DATA */
      headers={["", "Email", "First Name", "Last Name", "Mobile No."]}
      data={appsContent}
    />


    <hr style={{ margin: '5vh 0 5vh 0', width: '100%' }} />


    <div className="e-doc-editor">

      <div className="e-doc-views">
        <button id="e-doc-edit-btn"
          style={{ backgroundColor: '#c44444' }}
          onClick={
          () => {
            const btn = document.getElementById('e-doc-edit-btn') as HTMLElement;
            const otherBtn = document.getElementById('e-doc-preview-btn') as HTMLElement;
            const editor = document.getElementById('e-doc-edit-content') as HTMLInputElement;
            const content = document.getElementById('e-doc-content') as HTMLElement;
            btn.style.backgroundColor = '#c44444';
            otherBtn.style.backgroundColor = 'rgba(33,33,33,.66)';
            editor.style.display = 'block';
            content.style.display = 'none';
          }
        }> Editor </button>

        <button id="e-doc-preview-btn" style={{ borderRight: "2px solid rgba(33,33,33,0.99)" }} onClick={
          () => {
            const btn = document.getElementById('e-doc-preview-btn') as HTMLElement;
            const otherBtn = document.getElementById('e-doc-edit-btn') as HTMLElement;
            const editor = document.getElementById('e-doc-edit-content') as HTMLInputElement;
            const content = document.getElementById('e-doc-content') as HTMLElement;
            btn.style.backgroundColor = '#c44444';
            otherBtn.style.backgroundColor = 'rgba(33,33,33,.66)';
            editor.style.display = 'none';
            content.style.display = 'block';
            updateChanges();
          }
        }> Preview </button>

        <div className="right">
          <a href="https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started">
            Learn HTML
          </a>
          <a href="/" style={{ borderRight: "2px solid rgba(33,33,33,0.99)" }}> Options </a>
        </div>

      </div>

      <div
        id="e-doc-content"
        className="e-doc-content"
        style={{ display: "none" }}
      >{`${htmlContent}`}</div>

      <textarea
        id="e-doc-edit-content"
        className="e-doc-edit-content"
        onKeyPress={updateChanges}
        placeholder="&#13;
        HINTS & TIPS ------------------------------------------------------------- &#13;&#13;

        You can make a line of text a 'header' using an 'h' tag. To create one: &#13;
        you'll need to use a number ranging from 1 to 6 &#13;
        (smaller number = larger font size) <h1>, <h2>, <h3>, <h4>, <h5> or <h6> &#13;
        enter your text within the context of the tag like so; <h2> my title </h2> &#13;&#13;

        You can also add bold text with the <b> tag. &#13;
        Italic text with the <i> tag. &#13;
        or a link with the <a> tag. (<a href='www...com'> click here </a>) &#13;&#13;

        Click the `Learn More` Button to read a guide about creating HTML Documents &#13;&#13;

        --------------------------------------------------------------------------- &#13;&#13;"
      >{`${htmlContent}`}</textarea>

      <div className="e-doc-bottom-toolbar">
        <button style={{ backgroundColor: 'rgba(0,0,0,0)' }} onClick={removeChanges}> Remove Changes </button>
        <button type='submit' onClick={() => {
          updateChanges(); const editor = document.getElementById('e-doc-edit-content') as HTMLInputElement; POST(
            `job/attach/${encodeURIComponent(URL.uid)}`,
            editor.value,
            (resp:any) => alert(`[ERROR attaching HTML to JobPost entry ${URL.uid}] ${resp}`),
            (resp:any) => { alert('Content Saved Successfully.'); }
          )
        }}> Save </button>
      </div>
    </div>

  </>
}

export default JobsEdit;
