from django.urls import path
from core.views import asset_manifest, index, robots
from api.views import journal_list, journal_fetch

urlpatterns = [
    # Core Paths
    path('', index),
    path('robots.txt', robots),
    path('asset-manifest.json', asset_manifest),
    # Journal API Paths
    path('journal/list', journal_list),
    path('journal/fetch/<int:entry_id>', journal_fetch),
]
