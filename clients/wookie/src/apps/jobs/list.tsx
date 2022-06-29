// Local imports
import '../global.css';
// React imports
import { useState, useEffect } from 'react';
// Shared components
import Table from '../../shared/components/tables/table';
// Shared library
import { create_job_from_gui } from '../../shared/library/local/job';
import api from '../../shared/library/server/api';

const tableTitle = "Jobs";
const docTitle = `[E Panel] ${tableTitle}`;
const apiURL = "job/";


/*
  CREATE NEW JOB VIEW
  contains a modal with a create new job form
*/
const CreateView = (props: any) => <div className="full-modal">
  <div className="modal-form">

    <h1 className="tableHeader"> NEW [ JOB ] POST </h1>

      <div className="table-inputs">

        <label htmlFor="job_title"> Job Title <h6> This is the only required value. </h6> </label>
        <input className="table-input" type="text" id="job_title" name="job_title" placeholder="Job Title" required/>

        <label htmlFor="job_client"> Company (Client) <h6> This value is hidden from the applicant. </h6> </label>
        <input className="table-input" type="text" id="job_client" name="job_client" placeholder="Easter Company LTD" />

        <label htmlFor="location"> Location <h6> Leave blank if the job is remote. </h6> </label>
        <input className="table-input" type="text" id="job_location" name="job_location" placeholder="Remote" />

        <label htmlFor="job_min_salary">
          Salary (Range)
          <h6>
            Leave 'max' field blank to set a 'fixed' advertised salary or leave both fields blank for 'competitive'.
          </h6>
        </label>

        <div style={{display: 'flex', margin: '0 auto', maxWidth: '600px'}}>
          <input
            className="table-input" type="number"
            id="min_salary" name="min_salary"
            style={{ width: '280px' }}
            placeholder="min salary"
            required
          />
          <h6 style={{margin: 'auto 10px auto 10px'}}> to </h6>
          <input
            className="table-input" type="number"
            id="max_salary" name="max_salary"
            style={{ width: '280px' }}
            placeholder="max salary"
          />

        </div>
      </div>
  </div>

  <div className="flex-center">
    <button onClick={() => props.close()}> Cancel </button>
    <button type="submit" onClick={async () => {
      const title_el = document.getElementById("job_title") as HTMLInputElement;
      let job_title = title_el.value;

      if (job_title === "") title_el.style.backgroundColor = 'red';
      else job_title = encodeURIComponent(job_title)

      const client_el = document.getElementById("job_client") as HTMLInputElement;
      let job_client = client_el.value;
      if (job_client === "") job_client = "Anonymous";

      const location_el = document.getElementById("job_location") as HTMLInputElement;
      let job_location = location_el.value;
      if (job_location === "") job_location = "Remote";

      const min_salary_el = document.getElementById("min_salary") as HTMLInputElement;
      let min_salary = min_salary_el.value;
      if (min_salary === "") min_salary = "0";

      const max_salary_el = document.getElementById("max_salary") as HTMLInputElement;
      let max_salary = max_salary_el.value;
      if (max_salary === "") max_salary = "0";

      return create_job_from_gui(
        job_title,
        job_client,
        job_location,
        min_salary,
        max_salary
      )

    }}> Save & Submit </button>

  </div>

</div>


/*
  JOBS TABLE
  contains a generic table which outputs local database job data
*/
const JobsList = () => {
  const [head, setHead] = useState([]);
  const [body, setBody] = useState([]);

  useEffect(() => {

    const updateTable = () => {
      api(
        apiURL + 'list',
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
    name={"JOBS"}
    previewSize={50}

    /* TABLE DATA */
    headers={head}
    data={body}

    /* API PATHS */
    view={'get'}
    create={'create'}
    delete={'job/delete'}

    /* ACTION VIEWS */
    CreateView={CreateView}
  />
}

export default JobsList;
