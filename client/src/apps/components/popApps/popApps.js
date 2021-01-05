import './popApps.css'
import newIcon from '../../../assets/icons/pen.svg'
import oldIcon from '../../../assets/icons/journal.svg'
import nwfIcon from '../../../assets/icons/news.svg'


const toolbarButtons = [
    'journal-new', 'journal-old', 'journal-nwf'
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


const journalNewPressed = () => {toolbarButtonPress('journal-new')}
const journalOldPressed = () => {toolbarButtonPress('journal-old')}
const journalNwfPressed = () => {toolbarButtonPress('journal-nwf')}


const PopApps = () => {
    return <div id='document-body' className='document-body'>
        <div id='popApp-container-journal' className='popApp-container-selected'>
            <div id='app-toolbar-container' className='app-toolbar-container'>
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
            <h1>
                Sample text
            </h1>
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
