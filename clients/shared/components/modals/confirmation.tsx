// Shared Components
import './modal.css';


const ConfirmationModal = (props: any) => <div className="full-modal">

    <div className="full-modal-query">
        <h1 className="modal-header" style={{textAlign: "center", width: "100%"}}> {props.modal.header} </h1>
        <p style={{textAlign: 'center'}}> Are you sure you want to {props.modal.message} ? </p>
    </div>

    <div className="full-modal-options">

        <button onClick={() => {
            props.modal.cancel()
        }}> Cancel </button>

        <button type="submit" onClick={() => {
            props.modal.accept()
        }}> Accept </button>

    </div>
</div>


export default ConfirmationModal;
