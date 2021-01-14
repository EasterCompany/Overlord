from django.http import JsonResponse
from .journal import fetch
from .journal import post


# ========== FETCH API VIEWS ========== #


def journal_fetch_user_entries(req, user_id, *args, **kwargs):
    return JsonResponse(
        fetch.user_entries(user_id)
    )


def journal_fetch_entry(req, entry_id, *args, **kwargs):
    return JsonResponse(
        fetch.entry(entry_id)
    )


def journal_fetch_user_latest(req, user_id, *args, **kwargs):
    return JsonResponse(
        fetch.latest_entry(user_id)
    )


# ========== POST API VIEWS ========== #


def journal_post_user_entry(
    req, uid, token, head,
    body, image, public,
    *args, **kwargs
    ):
    # Parameter mutation
    if image == '0': image = None
    # API Function
    return JsonResponse(
        post.entry(uid, head, body, image, public)
    )
