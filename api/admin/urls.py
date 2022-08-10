# Django imports
from django.urls import path
# Overlord-API imports
from api.admin import views as Admin

API = lambda endpoint: f"api/panel/{endpoint}"
URLS = [

  #
  # Admin Panel API Endpoints
  #

  path(
    API("user/<str:uuid>"),
    Admin.view_user,
    name="View Users Panels"
  ),

  path(
    API("view/<str:uuid>"),
    Admin.view_panel,
    name="View Panel Details"
  ),

  path(
    API("create/<str:uuid>/<str:app_name>/<str:api_url>"),
    Admin.create,
    name="Create New Panel"
  ),

]
