from django.http import JsonResponse
from .journal import fetch


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
