from django.urls import path
from core.views import asset_manifest, index, robots
from api.views import journal_fetch_entry, journal_fetch_user_entries, \
    journal_fetch_user_latest, journal_post_user_entry

urlpatterns = [
    # Core Paths
    path('', index),
    path('robots.txt', robots),
    path('asset-manifest.json', asset_manifest),
    # Journal FETCH API Paths
    path('journal/fetch/<user_id>/entries', journal_fetch_user_entries),
    path('journal/fetch/<user_id>/latest', journal_fetch_user_latest),
    path('journal/entry/<int:entry_id>', journal_fetch_entry),
    # Journal POST API Paths
    path('journal/post/<uid>/<token>/<head>/<body>/<image>/<public>',
        journal_post_user_entry
    ),
]
