# Django imports
from django.urls import path
# Overlord-API imports
from api.admin import views as Admin

API = lambda endpoint: f"api/panel/{endpoint}"
URLS = [

  #
  # Admin Panel API Endpoints
  #

  # --- STATUS ---
  path(
    "api",
    Admin.api_status_check,
    name="Check API Status"
  ),

  # --- VIEW ---

  path(
    API("user/<str:uuid>"),
    Admin.view_user,
    name="View Users Panels"
  ),

  path(
    API("view/<str:pid>"),
    Admin.view_panel,
    name="View Panel Details"
  ),

  path(
    API("view/<str:pid>/users"),
    Admin.view_panel_users,
    name="View Panel Users"
  ),

  # --- CREATE ---

  path(
    API("create/<str:uuid>/<str:app_name>/<str:api_url>"),
    Admin.create,
    name="Create New Panel"
  ),

  path(
    API("verify/user/<str:pid>/<str:uuid>"),
    Admin.verify_user,
    name="Verify User on Panel"
  ),

  # --- UPDATE ---

  path(
    API("update/name/<str:pid>"),
    lambda req, pid, *args, **kwargs: Admin.update_setting(req, pid, 1, Admin.update_application_name_setting),
    name="Update Application Name Setting"
  ),

  path(
    API("update/api/<str:pid>"),
    lambda req, pid, *args, **kwargs: Admin.update_setting(req, pid, 1, Admin.update_application_api_setting),
    name="Update Application API Setting"
  ),

]
