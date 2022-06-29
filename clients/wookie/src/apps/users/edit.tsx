// Local imports
import '../global.css';
// Shared imports
import api from '../../shared/library/server/api';


/*
    EDIT USER VIEW
    requires a unique email which belongs to a verified account
    as a dynamic url parameter.
*/
const UserEdit = () => {
    document.title = '[E PANEL] Edit User';

    return <>
    <h2 style={{textAlign: 'center'}}> Edit User Account </h2>
    <form
        className="grid-section"
        style={{ maxWidth:"600px", margin: "0 auto", minWidth: "300px" }}
        action={`${api}user/edit`}
    >

        <h3> Basic Account Information </h3>
        <hr style={{minWidth:"100%"}}/>

        <label htmlFor="first_name" className="grid-item-head"> First Name </label>
        <input type="text" name="first_name" id="user_first_name" className="grid-item"/>

        <label htmlFor="last_name" className="grid-item-head"> Last Name </label>
        <input type="text" name="last_name" id="user_last_name" className="grid-item"/>

        <label htmlFor="email" className="grid-item-head"> Email Address </label>
        <input type="email" name="email" id="user_email" className="grid-item"/>

        <label htmlFor="date_of_birth" className="grid-item-head"> Date of Birth </label>
        <input type="date" name="date_of_birth" id="user_dob" className="grid-item"/>

        <label htmlFor="password" className="grid-item-head"> Password </label>
        <input type="password" name="password" id="user_password" className="grid-item"/>

        <label htmlFor="confirm_password" className="grid-item-head"> Password Again </label>
        <input type="password" name="confirm_password" id="user_confirm_password" className="grid-item"/>

        <hr style={{minWidth:"100%"}}/>
        <h3> Public User Profile </h3>
        <hr style={{minWidth:"100%"}}/>

        <div style={{ display: 'flex' }}>

            <div style={{ display: 'block', margin: '32px 0' }}>
                <label htmlFor="display_name" className="grid-item-head" style={{ margin: '0 auto' }}
                > Display Name </label>
                <input
                    type="text" id="user_display_name" className="grid-item"
                    name="display_name" placeholder="Display Name"
                />
                <label className="control checkbox">
                    <input type="checkbox" />
                    <span className="control-indicator" />
                    <h6> Use display name for public appearance </h6>
                </label>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', textAlign: 'right', alignItems: 'end' }}>
                <img
                    alt="user-profile"
                    className="profile-pic"
                />
                <input name="display_image" id="user_display_image" type="file" accept="image/*"/>
            </div>

        </div>
        <hr style={{minWidth:"100%"}}/>
        <button className="accept grid-item-head" type="button"> Save & Exit </button>

    </form></>
}


export default UserEdit;
