from django.urls import path
from core.views import asset_manifest, index, robots
from api.views import journal_fetch_entry, journal_fetch_user_entries, \
    journal_fetch_user_latest

urlpatterns = [
    # Core Paths
    path('', index),
    path('robots.txt', robots),
    path('asset-manifest.json', asset_manifest),
    # Journal API Paths
    path('journal/user/<user_id>/entries', journal_fetch_user_entries),
    path('journal/user/<user_id>/latest', journal_fetch_user_latest),
    path('journal/entry/<int:entry_id>', journal_fetch_entry),
]
