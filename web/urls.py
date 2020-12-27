from django.urls import path
from core.views import asset_manifest, index, robots
from api.views import journal_fetch_entry, journal_fetch_user_entries

urlpatterns = [
    # Core Paths
    path('', index),
    path('robots.txt', robots),
    path('asset-manifest.json', asset_manifest),
    # Journal API Paths
    path('journal/<user_id>/entries', journal_fetch_user_entries),
    path('journal/entry/<int:entry_id>', journal_fetch_entry),
]
