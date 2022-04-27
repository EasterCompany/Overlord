// Local imports
import '../edit.css';
import '../global.css';
// React imports
import { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
// Shared library
import api, { clientAdr, POST } from '../../shared/library/server/api';
// Shared components
import ConfirmationModal from '../../shared/components/modals/confirmation';

const tableTitle = "Edit Post";
const docTitle = `[E-PANEL] ${tableTitle}`;
const apiURL = "post/";

let initialContent = ``;


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
  POSTS VIEW & EDIT
  display all data on a post entry with options to edit certain values
*/
const PostsEditView = () => {
  const [deleteView, setDeleteView] = useState(false);
  const [htmlContent, setHtmlContent] = useState("");
  const URL:any = useParams()

  const editView = (open:boolean, save:boolean) => {
    const postHeader = document.getElementById("post_header") as HTMLElement;
    const postHeaderInput = document.getElementById("post_header_input") as HTMLInputElement;
    postHeader.style.display = open ? "none" : "block";
    postHeaderInput.style.display = open ? "block" : "none";

    const postSubheader = document.getElementById("post_subheader") as HTMLElement;
    const postSubheaderInput = document.getElementById("post_subheader_input") as HTMLInputElement;
    postSubheader.style.display = open ? "none" : "block";
    postSubheaderInput.style.display = open ? "block" : "none";

    const postLocation = document.getElementById("post_location") as HTMLElement;
    const postLocationInput = document.getElementById("post_location_input") as HTMLInputElement;
    postLocation.style.display = open ? "none" : "block";
    postLocationInput.style.display = open ? "block" : "none";

    const postCategory = document.getElementById("post_category") as HTMLElement;
    const postCategoryInput = document.getElementById("post_category_input") as HTMLInputElement;
    postCategory.style.display = open ? "none" : "block";
    postCategoryInput.style.display = open ? "block" : "none";

    const postLink = document.getElementById("post_link") as HTMLElement;
    const postLinkInput = document.getElementById("post_link_input") as HTMLInputElement;
    postLink.style.display = open ? "none" : "block";
    postLinkInput.style.display = open ? "block" : "none";

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
        `update/${encodeURIComponent(URL.uid)}/${encodeURIComponent(postHeaderInput.value)}/` +
        `${encodeURIComponent(postSubheaderInput.value)}/${encodeURIComponent(postLocationInput.value)}/` +
        `${encodeURIComponent(postCategoryInput.value)}/${encodeURIComponent(postLinkInput.value)}`,

        (resp: any) => alert(`[ERROR updating post entry for ${URL.uid}] ${resp}`),
        (resp: any) => {
          postHeader.innerText = postHeaderInput.value;
          postSubheader.innerText = postSubheaderInput.value;
          postLocation.innerText = postLocationInput.value;
          postCategory.innerText = postCategoryInput.value;
          postLink.innerText = postLinkInput.value;
        }
      );
    }
  }

  useEffect( () => {
    const fetchPostData = () => {
      api(
        apiURL + `get/${URL.uid}`,
        (resp: any) => alert(`[ERROR acquiring post entry ${URL.uid}] ${resp}`),
        (resp: any) => {

          const postHeader = document.getElementById("post_header") as HTMLElement;
          const postHeaderInput = document.getElementById("post_header_input") as HTMLInputElement;
          postHeader.innerHTML = resp.header;
          postHeaderInput.value = resp.header; postHeaderInput.style.display = "none";

          const postSubheader = document.getElementById("post_subheader") as HTMLElement;
          const postSubheaderInput = document.getElementById("post_subheader_input") as HTMLInputElement;
          postSubheader.innerHTML = resp.subheader;
          postSubheaderInput.value = resp.subheader; postSubheaderInput.style.display = "none";

          const postLocation = document.getElementById("post_location") as HTMLElement;
          const postLocationInput = document.getElementById("post_location_input") as HTMLInputElement;
          postLocation.innerHTML = resp.location;
          postLocationInput.value = resp.location; postLocationInput.style.display = "none";

          const postCategory = document.getElementById("post_category") as HTMLElement;
          const postCategoryInput = document.getElementById("post_category_input") as HTMLInputElement;
          postCategory.innerHTML = resp.category;
          postCategoryInput.value = resp.category; postCategoryInput.style.display = "none";

          const postLink = document.getElementById("post_link") as HTMLElement;
          const postLinkInput = document.getElementById("post_link_input") as HTMLInputElement;
          postLink.innerHTML = resp.link;
          postLinkInput.value = resp.link; postLinkInput.style.display = "none";

          const postDate = document.getElementById("post_date") as HTMLElement;
          postDate.innerHTML = resp.date;

          const contentBox = document.getElementById("e-doc-content") as HTMLElement;
          const editBox = document.getElementById("e-doc-edit-content") as HTMLInputElement;
          contentBox.innerHTML = resp.body;
          editBox.innerHTML = resp.body;
          initialContent = resp.body;

        }
      )
    }

    if (document.title !== docTitle) {
      document.title = docTitle;
      fetchPostData();
    }

  })

  if (deleteView) {
    const modal = {
      header: `DELETE [ GENERIC ] POST`,
      message: `delete ${URL.uid}`,
      accept: () => {
        api(
          `post/delete/${encodeURIComponent(URL.uid)}`,
          (resp: any) => alert(`[ERROR deleting post entry ${URL.uid}] ${resp}`),
          (resp: any) => window.location.href = clientAdr + 'posts'
        );
      },
      cancel: () => window.location.reload()
    }
    return <ConfirmationModal modal={modal} />
  }

  return <>
    <div id="edit-panels-top-row">

      <div id="edit-panel-left">

        <h2 id="post_header"> Header </h2>
        <input id="post_header_input" placeholder="Post Header" />

        <h3 id="post_subheader"> Subheader </h3>
        <input id="post_subheader_input" placeholder="Post Subheader" />

        <hr style={{ width: '100%' }}/>

        <h4 id="post_location"> Location </h4>
        <input id="post_location_input" placeholder="Post Location" />

        <h4 id="post_category"> Category </h4>
        <input id="post_category_input" placeholder="Post Category" />

        <h4 id="post_link"> Link </h4>
        <input id="post_link_input" placeholder="Post Link" />

        <h4 id="post_date"> Date </h4>

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
            `post/attach/${encodeURIComponent(URL.uid)}`,
            editor.value,
            (resp:any) => alert(`[ERROR attaching HTML to Post entry ${URL.uid}] ${resp}`),
            (resp:any) => { alert('Content Saved Successfully.'); }
          )
        }}> Save </button>
      </div>

    </div>

  </>
}

export default PostsEditView;
