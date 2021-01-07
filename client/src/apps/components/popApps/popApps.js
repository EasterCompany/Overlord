import './popApps.css'
import { shortDate } from '../../../library/dateTime.js'
import camera from '../../../assets/icons/camera.svg'
import newIcon from '../../../assets/icons/pen.svg'
import oldIcon from '../../../assets/icons/journal.svg'
import nwfIcon from '../../../assets/icons/news.svg'
import expIcon from '../../../assets/icons/expand.svg'

let toolbarTrayOpen = false;

const toolbarButtons = [
    'journal-new', 'journal-old', 'journal-nwf'
]

const journalViews = [
    'newentry', 'myentries', 'newsfeed'
]


const addImagePreview = () => {
    const imgEl = document.getElementById('journal-new-entry-img-upload')
    const cntEl = document.getElementById('journal-new-entry-img-container')
    imgEl.addEventListener('change', function() {
        const newImg = imgEl.files[0]
        if (newImg) {
            const reader = new FileReader()
            reader.addEventListener('load', function() {
                cntEl.style.backgroundImage = `url(${this.result})`
                cntEl.style.border = '2px solid #3498DB'
            })
            cntEl.style.opacity = '66%'
            reader.readAsDataURL(newImg)
        }
    })
}


const toolbarButtonPress = (pressed) => {
    for (const btn in toolbarButtons) {

        const el = document.getElementById(
            'app-toolbar-' + toolbarButtons[btn]
        )

        if (toolbarButtons[btn] === pressed) {
            el.className = 'app-toolbar-button atb-selected'
        } else {
            el.className = 'app-toolbar-button'
        }

    }
    // CLOSE NAVBAR TRAY ON MOBILE AFTER SELECTING AN OPTION
    document.getElementById('app-toolbar-expander').style.transform =
        'scaleY(1)'
    document.getElementById('app-toolbar-container').className =
        'app-toolbar-container hideOnMobile'
    toolbarTrayOpen = false
}


const toolbarExpanderPress = () => {
    const el = document.getElementById('app-toolbar-expander')
    const tb = document.getElementById('app-toolbar-container')

    if (toolbarTrayOpen) {
        el.style.transform = 'scaleY(1)'
        tb.className = 'app-toolbar-container hideOnMobile'
        toolbarTrayOpen = false
    } else {
        el.style.transform = 'scaleY(-1)'
        tb.className = 'app-toolbar-container showOnMobile'
        toolbarTrayOpen = true
    }

}


const journalViewSelect = (selected) => {
    for(const i in journalViews){
        const el = document.getElementById('popApp-journal-' + journalViews[i])
        if (selected === journalViews[i]) {
            el.style.display = 'block'
        } else {
            el.style.display = 'none'
        }
    }
}


const journalNewPressed = () => {
    toolbarButtonPress('journal-new')
    journalViewSelect('newentry')
}


const journalOldPressed = () => {
    toolbarButtonPress('journal-old')
    journalViewSelect('myentries')
}


const journalNwfPressed = () => {
    toolbarButtonPress('journal-nwf')
    journalViewSelect('newsfeed')
}


const PopApps = () => {
    return <div id='document-body' className='document-body'>
        <img
            id='app-toolbar-expander'
            alt='expanding arrow icon'
            className='app-toolbar-expander'
            src={expIcon}
            onClick={toolbarExpanderPress}
        />

        {/* ------------------ JOURNAL APP ------------------ */}
        <div id='popApp-container-journal' className='popApp-container-selected'>
            <div
                id='app-toolbar-container'
                className='app-toolbar-container hideOnMobile'
            >
                <img
                    id='app-toolbar-journal-nwf'
                    src={nwfIcon}
                    alt='news feed button'
                    className='app-toolbar-button atb-selected'
                    onClick={journalNwfPressed}
                />
                <img
                    id='app-toolbar-journal-new'
                    src={newIcon}
                    alt='new entry button'
                    className='app-toolbar-button'
                    onClick={journalNewPressed}
                />
                <img
                    id='app-toolbar-journal-old'
                    src={oldIcon}
                    alt='my entries button'
                    className='app-toolbar-button'
                    onClick={journalOldPressed}
                />
            </div>

            <div id='popApp-journal-newsfeed'>
                <h1>
                    News Feed
                </h1>
            </div>

            <form id='popApp-journal-newentry'>
                <div style={{display:'flex'}}>
                    <div className='journal-entry-head-divider' />
                    <input
                        id='journal-new-entry-head'
                        name='title'
                        required
                        maxLength='90'
                        placeholder='New Entry'
                    />
                    <div className='journal-entry-head-divider' />
                </div>
                <textarea
                    id='journal-new-entry-body'
                    name='content'
                    required
                    placeholder='Write your entry here...'
                />
                <label id='journal-new-entry-img-container' onClick={addImagePreview}>
                    <input id='journal-new-entry-img-upload' type='file' hidden />
                    <img
                        src={camera}
                        style={{
                            width:'fit-content'
                        }}
                        alt='upload'
                    />
                    <h6
                        style={{
                            width:'100%',
                            textAlign:'center',
                            color:'lightgrey'
                        }}
                    >
                        upload an image
                    </h6>
                </label>
                <div style={{
                    width:'40%',
                    minWidth:'300px',
                    display:'flex',
                    margin:'6px auto 6px auto',
                    justifyContent:'space-between'
                }}>
                    <p className='journal-new-entry-detail' style={{textAlign:'left'}}>
                        Owen Cameron Easter
                    </p>
                    <p className='journal-new-entry-detail' style={{textAlign:'right'}}>
                        {shortDate()}
                    </p>
                </div>
                <button id='journal-new-entry-submit' type='submit'>
                    <p> Submit </p>
                </button>
            </form>

            <div id='popApp-journal-myentries'>
                <h1>
                    View my entries
                </h1>
            </div>

        </div>

        {/* ------------------ FINANCE APP ------------------ */}
        <div id='popApp-container-finance' className='popApp-container'>
            <h1> Finance </h1>
        </div>

        {/* ------------------ DISCOVER APP ------------------ */}
        <div id='popApp-container-discover' className='popApp-container'>
            <h1> Discover </h1>
        </div>

    </div>
}


export default PopApps
