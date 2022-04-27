// Shared Components
import './modal.css';


const AdminLoginModal = (props: any) => <div className="full-modal">
    <div>
        <h1 className="tableHeader" style={{textAlign: "center", width: "100%"}}> [ADMIN] LOGIN </h1>
        <label> EMAIL </label>
        <input id="admin-email" name="admin-email" type="email"/>
        <label> PASSWORD </label>
        <input id="admin-pass" name="admin-pass" type="password"/>
    </div>
    <div className="flex-center">

        <button onClick={() => {
            window.location.reload()
        }}> Cancel </button>

        <button type="submit" onClick={() => {
            window.location.reload()
        }}> Accept </button>

    </div>
</div>


export default AdminLoginModal;