import './popApps.css'
import sanitize from '../../../library/sanitize.js'
import camera from '../../../assets/icons/camera.svg'
import newIcon from '../../../assets/icons/pen.svg'
import oldIcon from '../../../assets/icons/journal.svg'
import nwfIcon from '../../../assets/icons/news.svg'
import expIcon from '../../../assets/icons/expand.svg'
import ex2Icon from '../../../assets/icons/expand2.svg'
import { shortDate, date } from '../../../library/dateTime.js'

let toolbarTrayOpen = false;
let entryImg = null;

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
                entryImg = this.result
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


const longJournalExpanderPress = (pid) => {
    const el = document.getElementById(`pid_${pid}`);
    const ex = document.getElementById(`pid_${pid}_expander`);
    const im = document.getElementById(`pid_${pid}_expanderImg`);
    if(el.style.maxHeight !== 'unset') {
        el.style.maxHeight = 'unset';
        el.style.overflowY = 'visible';
        ex.style.height  = '36px';
        ex.style.marginTop = '-16px';
        ex.style.paddingTop = 'unset';
        im.style.transform = 'scaleY(-1)';
    } else {
        el.style.maxHeight = '';
        el.style.overflowY = '';
        ex.style.height  = '';
        ex.style.marginTop = '';
        ex.style.paddingTop = '';
        im.style.transform = '';
    }
}


const makeEntry = (pid, head, body, img=null) => {
    if (img) img = `<img src='${img}' class='journal-entry-img'>`
    else img = ``

    head = sanitize(head)
    body = sanitize(body)

    if (body.length > 999){
        return `
        <div class='journal-entry'>
            ${img}
            <p class='journal-entry-head'> ${head} </p>
            <p class='journal-entry-time'> ${date()} </p>
            <p id='pid_${pid}' class='journal-entry-body-long'>
                ${body}
            </p>
            <div
                id='pid_${pid}_expander'
                class='journal-entry-expander'
                onClick="
                    const expand = ${longJournalExpanderPress};
                    expand('${pid}');
                "
            >
                <img
                    id='pid_${pid}_expanderImg'
                    class='journal-entry-expander-img'
                    src='${ex2Icon}'
                >
            </div>
        </div>
        `
    } else {
        return `<div class='journal-entry'>
            ${img}
            <p class='journal-entry-head'> ${head} </p>
            <p class='journal-entry-time'> ${date()} </p>
            <p class='journal-entry-body'> ${body} </p>
        </div>`
    }
}


const newEntrySubmit = () => {
    // UPDATE 'My Entries' with new Entry data
    const entryHead = document.getElementById('journal-new-entry-head')
    const entryBody = document.getElementById('journal-new-entry-body')

    if (entryHead.value.length > 0 && entryBody.value.length > 0) {
        const feed = document.getElementById('journal-myentries-feed')
        feed.innerHTML = makeEntry(
            entryHead.value, entryHead.value, entryBody.value, entryImg
        ) + feed.innerHTML
        entryHead.value = ''
        entryBody.value = ''
        entryImg = null
        const entryImgUp = document.getElementById(
            'journal-new-entry-img-container'
        )
        entryImgUp.style.backgroundImage = 'none'
        entryImgUp.style.border = ''
        // RETURN function by emulating press 'My Entries'
        return journalOldPressed()

    } else {
        // UPDATE 'New Entry' with invalid inputs error
        if (entryHead.value.length === 0) {
            entryHead.classList.add('submit-error')
            document.getElementById('submit-error-no-head').style.display = 'block'
        }
        if (entryBody.value.length === 0) {
            entryBody.classList.add('submit-error')
            document.getElementById('submit-error-no-body').style.display = 'block'
        }
    }

}


const newEntryHeadClick = () => {
    document.getElementById(
        'journal-new-entry-head'
    ).classList.remove('submit-error')
    document.getElementById(
        'submit-error-no-head'
    ).style.display = 'none'
}


const newEntryBodyClick = () => {
    document.getElementById(
        'journal-new-entry-body'
    ).classList.remove('submit-error')
    document.getElementById(
        'submit-error-no-body'
    ).style.display = 'none'
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

            <div id='popApp-journal-newentry'>
                <div style={{display:'flex'}}>
                    <div className='journal-entry-head-divider' />
                    <input
                        id='journal-new-entry-head'
                        name='title'
                        required
                        maxLength='90'
                        placeholder='New Entry'
                        onClick={newEntryHeadClick}
                    />
                    <div className='journal-entry-head-divider' />
                </div>
                <p
                    id='submit-error-no-head'
                    className='submit-error-msg'
                > ・ You need to title your entry </p>
                <p
                    id='submit-error-no-body'
                    className='submit-error-msg'
                > ・ You need to write your entry </p>
                <textarea
                    id='journal-new-entry-body'
                    name='content'
                    required
                    placeholder='Write your entry here...'
                    onClick={newEntryBodyClick}
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
                <button
                    id='journal-new-entry-submit'
                    onClick={newEntrySubmit}
                >
                    Submit
                </button>
            </div>

            <div id='popApp-journal-myentries'>
                <div id='journal-myentries'>
                    <div className='journal-myentries-spacer'> &nbsp; </div>
                    <div id='journal-myentries-details'>
                        <img
                            alt='user'
                            src={camera}
                            className='journal-user-image'
                        />
                        <p style={{fontSize:'20px', textAlign:'center'}}>
                            Owen Cameron Easter
                        </p>
                        <div id='journal-myentries-userinfo'>
                            <p> <b>22</b> years old </p>
                            <p> Software Engineer </p>
                            <p> Easter Company </p>
                            <hr />
                            <p> Entries: <b>23</b> </p>
                            <p> Last Updated: 01/01/2021 </p>
                            <hr />
                            <div id='journal-myentries-followContainer'>
                                <div id='journal-myentries-followTags'>
                                    <p> Followers </p>
                                    <p> Following </p>
                                </div>
                                <div id='journal-myentries-followInfo'>
                                    <p> 25 </p>
                                    <p> 5000 </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id='journal-myentries-feed'>
                    </div>
                </div>
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
