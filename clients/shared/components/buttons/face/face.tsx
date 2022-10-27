import './face.css';


const FaceButton = (props:any) => <a
  className="face-button"
  href={props.href === undefined ? "#" : props.href}
  style={props.style === undefined ? {} : props.style}
>

  <div className="face-primary">
    {props.title}
  </div>

  <div className="face-secondary">
    {props.description}
  </div>

</a>


export default FaceButton;
