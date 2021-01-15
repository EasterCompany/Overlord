// LIBRARY IMPORTS
import sanitize from '../sanitize'
import { date } from '../dateTime'

// ASSET IMPORTS
import ex2Icon from '../../assets/icons/expand2.svg'
import prvIcon from '../../assets/icons/lock.svg'


export const longJournalExpanderPress = (pid) => {
    const id = 'pid_'.concat(pid);
    const el = document.getElementById(id);
    const ex = document.getElementById(id + '_expander');
    const im = document.getElementById(id + '_expanderImg');
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


export const makeEntry = (pid, user, head, body, img=null, isPublic, timeStamp) => {
    if (img) img = `<img src='${img}' class='journal-entry-img'>`
    else img = ``

    const stamp = new Date(timeStamp)
    const Type = isPublic ? `` : `
        <div class='journal-entry-type'>
            <img src='${prvIcon}' alt='private' />
        </div>`
    const Head = sanitize(head)
    const Body = sanitize(body)

    if (body.length > 999 || (body.match(/\n/g) || []).length >= 10){
        return `
        <div class='journal-entry'>
            ${Type}
            ${img}
            <p class='journal-entry-head'>${Head}</p>
            <div class='journal-entry-info'>
                <p class='journal-entry-user'>${user}</p>
                <p class='journal-entry-time'>${date(stamp)}</p>
            </div>
            <p id='pid_${pid}' class='journal-entry-body-long'>${Body}</p>
            <div
                id='pid_${pid}_expander'
                class='journal-entry-expander'
                onClick='
                    const expand = ${longJournalExpanderPress};
                    expand("${pid}");
                '
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
        return `
        <div class='journal-entry'>
            ${Type}
            ${img}
            <p class='journal-entry-head'>${Head}</p>
            <div class='journal-entry-info'>
                <p class='journal-entry-user'>${user}</p>
                <p class='journal-entry-time'>${date(stamp)}</p>
            </div>
            <p class='journal-entry-body'>${Body}</p>
        </div>
        `
    }
}


export default makeEntry
