import './popApps.css'
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
                <form>
                    <div style={{display:'flex'}}>
                        <div className='journal-entry-head-divider' />
                        <input
                            id='journal-new-entry-head'
                            required
                            maxLength='90'
                            placeholder='New Entry'
                        />
                        <div className='journal-entry-head-divider' />
                    </div>
                    <textarea
                        id='journal-new-entry-body'
                        required
                        placeholder='Write your entry here...'
                    />
                    <button id='journal-new-entry-submit' type='submit'>
                        Submit
                    </button>
                </form>
            </div>
            <div id='popApp-journal-myentries'>
                <h1>
                    View my entries
                </h1>
            </div>
        </div>

        <div id='popApp-container-finance' className='popApp-container'>
            <h1> Finance </h1>
        </div>

        <div id='popApp-container-discover' className='popApp-container'>
            <h1> Discover </h1>
        </div>
    </div>
}


export default PopApps
