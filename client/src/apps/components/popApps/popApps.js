// LIBRARY IMPORTS
import './popApps.css'
import { shortDate } from '../../../library/dateTime.js'
import {
    fetchMyEntries,
    submitEntry
} from '../../../library/journal/api.js'

// ASSET IMPORTS
import camera from '../../../assets/icons/camera.svg'
import userImg from '../../../assets/icons/user.svg'
import newIcon from '../../../assets/icons/edit.svg'
import oldIcon from '../../../assets/icons/book.svg'
import nwfIcon from '../../../assets/icons/newspaper.svg'
import expIcon from '../../../assets/icons/expand.svg'

// GLOBAL DECLERATIONS
let entryImg = null;
let toolbarTrayOpen = false;

const toolbarButtons = [
    'journal-new', 'journal-old', 'journal-nwf'
]

const journalViews = [
    'newentry', 'myentries', 'newsfeed'
]

// PROMISE DECLERATIONS
fetchMyEntries('123')


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


const newEntrySubmitPressed = () => {
    const entryHead = document.getElementById('journal-new-entry-head')
    const entryBody = document.getElementById('journal-new-entry-body')
    const privacyOp = document.getElementById('journal-new-entry-private')
    const post = submitEntry(
        entryHead.value,
        entryBody.value,
        entryImg,
        privacyOp.checked
    )
    if(post){
        // UPDATE 'My Entries' with new entry
        const feed = document.getElementById('journal-myentries-feed')
        const count = document.getElementById('journal-myentries-count')
        count.innerText = parseInt(count.innerText) + 1
        feed.innerHTML = post + feed.innerHTML
        // RESET 'New Entry' form to be empty
        const entryImgUp = document.getElementById(
            'journal-new-entry-img-container'
        )
        entryImg = null
        entryHead.value = ''
        entryBody.value = ''
        entryImgUp.style.backgroundImage = 'none'
        entryImgUp.style.border = ''
        privacyOp.checked = false
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
        return null
    }
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
                <input
                    id='journal-newsfeed-search'
                    placeholder='search users & entries'
                />
                <div id='journal-newsfeed-container'>
                    <div id='journal-sidefeed-container'>
                        <div id='journal-newsfeed-trends'>
                            <h5 style={{
                                marginBottom:'10px',
                                color:'darkgrey'
                            }}>
                                popular topic
                            </h5>
                            <img
                                id='journal-trend-img'
                                src={userImg}
                                alt='suggested trend'
                            />
                            <p id='journal-trend-name'
                            > Software </p>
                            <button
                                id='journal-feed-follow-btn'
                            > Follow </button>
                        </div>
                        <div id='journal-newsfeed-follow'>
                            <h5 style={{
                                marginBottom:'10px',
                                color:'darkgrey'
                            }}>
                                popular user
                            </h5>
                            <img
                                id='journal-trend-img'
                                src={userImg}
                                alt='suggested trend'
                            />
                            <p id='journal-trend-name'
                            > John Smitherssssss Smith </p>
                            <button
                                id='journal-feed-follow-btn'
                            > Follow </button>
                        </div>
                    </div>
                    <div id='journal-newsfeed'>
                    </div>
                </div>
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
                    <div>
                        <input
                            type='checkbox'
                            id='journal-new-entry-private'
                            value='private'
                        />
                        <label
                            htmlFor='journal-new-entry-private'
                            className='journal-new-entry-detail'
                        > Private Entry </label>
                    </div>
                    <p className='journal-new-entry-detail' style={{textAlign:'right'}}>
                        {shortDate()}
                    </p>
                </div>
                <button
                    id='journal-new-entry-submit'
                    onClick={newEntrySubmitPressed}
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
                            src={userImg}
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
                            <p> Entries:&nbsp;
                                <b id='journal-myentries-count'>
                                    0
                                </b>
                            </p>
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
