// Component imports
import './loading.css';
import loadingImg from '../../assets/icons/loading.svg';


const Loader = (props: any) => {
    return <div
        style={{display: props.state}}
        className="loading-asset"
    >
        <img
            className="loading-img"
            src={loadingImg}
            alt="loading"
        />
        <h3> Loading... </h3>
    </div>
}


export default Loader;
