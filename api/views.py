from django.http import JsonResponse
from .models import Entry


def journal_list(req, *args, **kwargs):
    qs = Entry.objects.all()
    entries = [
        {
            "pid": x.pid,
            "uid": x.uid,
            "head": x.head,
            "body": x.body,
            "likes": x.likes,
            "laughs": x.laughs,
            "sads": x.sads,
            "shares": x.shares
        } for x in qs
    ]
    return JsonResponse({'entries': entries})


def journal_fetch(req, entry_id, *args, **kwargs):
    data = {
        'id': entry_id
    }
    try:
        obj = Entry.objects.get(id=entry_id)
        data['status'] = 200
        data['content'] = obj.content
    except:
        data['status'] = 404
        data['content'] = ''
    return JsonResponse(
        data,
        status=data['status']
    )
