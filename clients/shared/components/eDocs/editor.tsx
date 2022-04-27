import { POST } from '../../library/server/api';


export const updateChanges = () => {
  const content = document.getElementById("e-doc-content") as HTMLElement;
  const editor = document.getElementById("e-doc-edit-content") as HTMLInputElement;
  content.innerHTML = editor.value;
  }


export const removeChanges = () => {
  const content = document.getElementById("e-doc-content") as HTMLElement;
  const editor = document.getElementById("e-doc-edit-content") as HTMLInputElement;
  content.innerHTML = '';
  editor.value = '';
}


export const Editor = (URL:any, htmlContent:any) => {
  return <div className="e-doc-editor">
    <div className="e-doc-views">
      <button id="e-doc-edit-btn"
      style={{ backgroundColor: '#c44444' }}
      onClick={() => {
        const btn = document.getElementById('e-doc-edit-btn') as HTMLElement;
        const otherBtn = document.getElementById('e-doc-preview-btn') as HTMLElement;
        const editor = document.getElementById('e-doc-edit-content') as HTMLInputElement;
        const content = document.getElementById('e-doc-content') as HTMLElement;
        btn.style.backgroundColor = '#c44444';
        otherBtn.style.backgroundColor = 'rgba(33,33,33,.66)';
        editor.style.display = 'block';
        content.style.display = 'none';
      }}> Editor </button>

      <button id="e-doc-preview-btn" style={{ borderRight: "2px solid rgba(33,33,33,0.99)" }} onClick={() => {
        const btn = document.getElementById('e-doc-preview-btn') as HTMLElement;
        const otherBtn = document.getElementById('e-doc-edit-btn') as HTMLElement;
        const editor = document.getElementById('e-doc-edit-content') as HTMLInputElement;
        const content = document.getElementById('e-doc-content') as HTMLElement;
        btn.style.backgroundColor = '#c44444';
        otherBtn.style.backgroundColor = 'rgba(33,33,33,.66)';
        editor.style.display = 'none';
        content.style.display = 'block';
        updateChanges();
      }}> Preview </button>

      <div className="right">
        <a href="https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started">
          Learn HTML
        </a>
        <a href="/" style={{ borderRight: "2px solid rgba(33,33,33,0.99)" }}>
          Options
        </a>
      </div>
    </div>
    <div
      id="e-doc-content"
      className="e-doc-content"
      style={{ display: "none" }}
    >
      {`${htmlContent}`}
    </div>
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
          (resp:any) => alert(`[ERROR attaching HTML to post entry ${URL.uid}] ${resp}`),
          (resp:any) => { alert('Content Saved Successfully.'); }
      )}}> Save </button>
    </div>
  </div>
}


export default Editor;
