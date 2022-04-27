// Local components
import './404.css';


const PageNotFoundError = () => {
  document.title = '[E PANEL] Error 404';

  return <div id="page-not-found" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
    <h2> Sorry, this page doesn't exist. </h2>
    <p style={{textAlign: 'center'}}>
      Perhaps you stumbled across something that doesn't exist yet..? <br/> ooo, isn't that exciting!
    </p>
  </div>
}


export default PageNotFoundError;
