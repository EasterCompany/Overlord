from api.models import JournalEntry


def entry(user, head, body, image, public):
    # TODO: link uid to user id from db
    # TODO: link token to user access token

    if len(user) == 0 or user != '123':
        return {'error': 'invalid user id'}
    if len(head) == 0 or len(head) > 90:
        return {'error': 'invalid entry head'}
    if len(body) == 0:
        return {'error': 'invalid entry body'}
    if image is not None:
        return {'error': 'invalid image type'}

    JournalEntry.objects.create(
        uid=user,
        head=head,
        body=body,
        public=public
    )
    return {'post': 'success!'}
