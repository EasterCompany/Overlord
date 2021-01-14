import makeEntry from './makeEntry'
import serverAdr from '../server'
import { date } from '../dateTime'


export const postMyEntry = (uid, token, head, body, image, isPublic) => {
    isPublic = isPublic ? '1' : '0'
    head = encodeURIComponent(head)
    body = encodeURIComponent(body)
    image = encodeURIComponent(image)
    fetch(
        `${serverAdr}journal/post/${uid}/${token}/${head}/${body}/${image}/${isPublic}`
    ).then(
        res => {
            res.json().then(
                data => {
                    if('error' in data){
                        console.log(data['error'])
                    }
                }
            )
        }
    )
}


export const submitEntry = (head, body, image, isPrivate) => {
    const isPublic = isPrivate ? false : true
    if (head.length > 0 && body.length > 0) {
        postMyEntry('123', '0', head, body, '0', isPublic)
        const post = makeEntry(
            head,
            'Owen Cameron Easter',
            head,
            body,
            image,
            isPublic,
            date()
        )
        return post
    }
    return null
}


export const makeMyEntries = (data) => {
    const feed = document.getElementById('journal-myentries-feed')
    const count = document.getElementById('journal-myentries-count')
    feed.innerHTML = ''
    count.innerText = data.length
    for(const entry in data){
        feed.innerHTML = feed.innerHTML + makeEntry(
            data[entry]['id'],
            data[entry]['uid'],
            data[entry]['head'],
            data[entry]['body'],
            data[entry]['image'],
            data[entry]['public'],
            data[entry]['timestamp']
        )
    }
}


// TODO: require token to fetch public & private user entries
export const fetchMyEntries = (uid, _token='0') => {
    fetch(`${serverAdr}journal/fetch/${uid}/entries`)
    .then(res => {
        res.json().then(
            data => {
                if (uid in data) {
                    makeMyEntries(data[uid])
                }
            }
        )
    })
}

