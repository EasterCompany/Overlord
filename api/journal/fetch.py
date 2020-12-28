from ..models import JournalEntry


def create_entry_dict(db_object):
    '''
    Converts an entry data dictionary from db object

    Parameters:
        db_object (obj): django database object

    Returns:
        dict: containing entry information
    '''
    if db_object is None:
        return {
            'error': 'invalid request'
        }
    return {
        'id': db_object.id,
        'uid': db_object.uid,
        'head': db_object.head,
        'body': db_object.body,
        'likes': db_object.likes,
        'laughs': db_object.laughs,
        'sads': db_object.sads,
        'shares': db_object.shares,
        'timestamp': db_object.timestamp,
        'public': db_object.public
    }


def fetch_error(excep):
    '''
    Converts exception to api-friendly format

    Parameters:
        excep (Exception): error message from try/except

    Returns:
        dict: containing error message as string
    '''
    return {
        'error': str(excep)
    }


def entry(entry_id):
    '''
    Fetches the entry associated with the entry_id

    Parameters:
        entry_id (str): unique id for specific entry

    Returns:
        dict: containing entry associated with a unique entry_id
    '''
    try:
        return create_entry_dict(
            JournalEntry.objects.get(id=entry_id)
        )
    except Exception as e:
        return fetch_error(e)


def user_entries(user_id):
    '''
    Fetches all entries associated with the user_id

    Parameters:
        user_id (str): unique id for specific user

    Returns:
        data (dict): containing all entries associated with a unique user_id
    '''
    try:
        entries = JournalEntry.objects.filter(uid=user_id)
        return {
            user_id: [create_entry_dict(obj) for obj in entries]
        }
    except Exception as e:
        return fetch_error(e)


def latest_entry(user_id):
    '''
    Fetches the latest entry associated with the user_id

    Parameters:
        user_id (str): unique id for specific user

    Returns:
        data (dict): containing latest entry from user
    '''
    try:
        return create_entry_dict(
            JournalEntry.objects.filter(uid=user_id).latest('id')
        )
    except Exception as e:
        return fetch_error(e)
