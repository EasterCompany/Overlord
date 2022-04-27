// Local imports
import '../global.css';
// React imports
import { useState, useEffect } from 'react';
// Shared components
import Table from '../../shared/components/tables/table';
// Shared library
import { create_post_from_gui } from '../../shared/library/local/post';
import api from '../../shared/library/server/api';

const tableTitle = "Posts";
const docTitle = `[E PANEL] ${tableTitle}`;
const apiURL = "post/";


/*
  CREATE NEW POST VIEW
  contains a modal with a create new post form
*/
const CreateView = (props: any) => <div className="full-modal">
  <div className="modal-form">

    <h1 className="tableHeader"> NEW [ GENERIC ] POST </h1>

    <div className="table-inputs">

        <label htmlFor="post_header"> Header </label>
        <input
        name="post_header"
        className="table-input"
        type="text" id="post_header"
        placeholder="Title your post"
        required
        />

        <label htmlFor="post_subheader"> Subheader </label>
        <input className="table-input" type="text" id="post_subheader" name="post_subheader" placeholder="N/A" />

        <label htmlFor="genre"> Genre (Category) </label>
        <input className="table-input" type="text" id="post_genre" name="post_genre" placeholder="N/A" />

        <label htmlFor="location"> Location </label>
        <input className="table-input" type="text" id="post_location" name="post_location" placeholder="N/A" />

        <label htmlFor="link"> Link </label>
        <input className="table-input" type="text" id="post_link" name="post_link" placeholder="N/A" />

        <label htmlFor="post_custom_tags"> custom tags (csv field)
            <h6>
            * Tags should be separated by commas (like, this, is)
            </h6>
        </label>

        <label htmlFor="post_custom_values"> custom values (json field)
            <h6>
            Contents is displayed as a table on the posts content page
            </h6>
        </label>

      <div className="flex-center">
        <button onClick={() => props.close()}> Cancel </button>
        <button
          type="submit"
          onClick={async () => {
            const title = document.getElementById("post_header") as HTMLInputElement;
            let post_title = title.value;

            if (post_title === "") title.style.backgroundColor = 'red';
            else post_title = encodeURIComponent(post_title)

            const subheader = document.getElementById("post_subheader") as HTMLInputElement;
            const location = document.getElementById("post_location") as HTMLInputElement;
            const genre = document.getElementById("post_genre") as HTMLInputElement;
            const link = document.getElementById("post_link") as HTMLInputElement;
            const custom_tags = document.getElementById("post_custom_tags") as HTMLInputElement;
            const custom_values = document.getElementById("post_custom_values") as HTMLInputElement;

            const URIComponent = (elInput:HTMLInputElement) => {
              if (elInput === null) return encodeURIComponent("-")
              return encodeURIComponent(elInput.value || "-")
            }

            return create_post_from_gui(
              post_title,
              URIComponent(subheader),
              URIComponent(location),
              URIComponent(genre),
              URIComponent(link),
              URIComponent(custom_values),
              URIComponent(custom_tags)
            )
        }}> Save & Submit </button>
      </div>
    </div>
  </div>
</div>


/*
  Posts TABLE
  contains a generic table which outputs local database Posts data
*/
const PostsList = () => {
  const [head, setHead] = useState([]);
  const [body, setBody] = useState([]);

  useEffect( () => {

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
    name={"POSTS"}
    previewSize={50}

    /* TABLE DATA */
    headers={head}
    data={body}

    /* API PATHS */
    view={'get'}
    create={'create'}
    delete={'post/delete'}

    /* ACTION VIEWS */
    CreateView={CreateView}
  />
}

export default PostsList;
