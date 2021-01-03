import './popApps.css'
import { selectedPopApp } from '../navbar/navbar.js'


const PopApps = () => {
    return <div id='document-body' className='document-body'>
        <p> {selectedPopApp} </p>
        <div id='popApp-journal-container' className='popApp-journal-container'>
            <h1> Journal </h1>
        </div>
        <div id='popApp-finance-container' className='popApp-finance-container'>
            <h1> Finance </h1>
        </div>
        <div id='popApp-discover-container' className='popApp-discover-container'>
            <h1> Discover </h1>
        </div>
    </div>
}


export default PopApps
