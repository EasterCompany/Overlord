import './download.css';


const DownloadButton = (props:any) => <a
  className="face-button"
  href={props.link}
>

  <div className="face-primary">
    <span className="icon fa fa-cloud"></span>
    {props.title}
  </div>

  <div className="face-secondary">
    <span className="icon fa fa-hdd-o"></span>
    {props.description}
  </div>

</a>


export default DownloadButton;
