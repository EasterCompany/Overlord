# Current API
from api.eastercompany.controls import create_new_panel
from . import API
from .controls import *

# --- VIEW ---
API.path(
  "list",
  lambda req, *args, **kwargs: list_all_recipes(),
  "List All Recipes"
)

API.path(
  "ingredients/list",
  lambda req, *args, **kwargs: list_all_ingredients(),
  "List All Ingredients"
)

API.path(
  "utensils/list",
  lambda req, *args, **kwargs: list_all_utensils(),
  "List All Utensils"
)

# --- CREATE ---
API.path(
  "utensils/create",
  lambda req, *args, **kwargs: create_new_utensils(req),
  "Create New Utensils Record"
)
