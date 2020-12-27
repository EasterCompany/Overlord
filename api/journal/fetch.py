from ..models import JournalEntry


def create_entry_dict(db_object):
    '''
    Converts an entry data dictionary from db object

    Parameters:
        db_object (obj): django database object

    Returns:
        dict: containing entry information
    '''
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


def fetch_exception(excep):
    '''
    Converts exception to api-friendly format

    Parameters:
        excep (Exception): error message from try/except

    Returns:
        dict: containing error message as string
    '''
    return {'error': str(excep)}


def entry(entry_id):
    '''
    Fetches the entry associated with the entry_id

    Parameters:
        entry_id (str): unique id for specific entry

    Returns:
        dict: containing entry associated with a unique entry_id
    '''
    try:
        obj = JournalEntry.objects.get(id=entry_id)
        return create_entry_dict(db_object=obj)
    except Exception as e:
        return fetch_exception(e)


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
        data = [create_entry_dict(obj) for obj in entries]
        return {user_id: data}
    except Exception as e:
        return fetch_exception(e)
