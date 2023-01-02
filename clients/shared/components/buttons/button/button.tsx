import './button.css';


const Button = (props:any) => <button
  style={props.style === undefined ? {} : props.style}
  onClick={props.onClick === undefined ? "" : props.onClick}
>
  {props.text}
</button>


export default Button;
