import './download.css';


const DownloadButton = ({ title, description, link, icon1, icon2 }:any) => <a
  className="face-button"
  href={link}
>

  <div className="face-primary">
    <span
      className={icon1 === undefined ? "icon fa-solid fa-download" : icon1}
      style={{ paddingRight: '12px' }}>
    </span>
    {title}
  </div>

  <div className="face-secondary">
    <span
      className={icon2 === undefined ? "icon fa-solid fa-hdd-o" : icon2}
      style={{ paddingRight: '12px' }}>
    </span>
    {description}
  </div>

</a>


export default DownloadButton;
