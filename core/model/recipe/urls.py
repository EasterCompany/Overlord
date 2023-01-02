# Current API
from . import API
from .controls import *

# --- VIEW ---
API.path(
  "list",
  lambda req, *args, **kwargs: list_all_recipes(),
  "List All Recipe"
)

API.path(
  "ingredients/list",
  lambda req, *args, **kwargs: list_all_ingredients(),
  "List All Ingredient"
)

API.path(
  "utensils/list",
  lambda req, *args, **kwargs: list_all_utensils(),
  "List All Utensil"
)

API.path(
  "foreign",
  lambda req, *args, **kwargs: list_foreign_keys(),
  "List Foreign Keys"
)

# --- CREATE ---
API.path(
  "create",
  lambda req, *args, **kwargs: create_new_recipe(req),
  "Create New Recipe Record"
)

API.path(
  "ingredients/create",
  lambda req, *args, **kwargs: create_new_ingredient(req),
  "Create New Ingredient Record"
)

API.path(
  "utensils/create",
  lambda req, *args, **kwargs: create_new_utensil(req),
  "Create New Utensil Record"
)

# --- DELETE ---
API.path(
  "delete",
  lambda req, *args, **kwargs: delete_recipe(api.get_json(req)['uuid']),
  "Delete Recipe Record"
)

API.path(
  "ingredients/delete",
  lambda req, *args, **kwargs: delete_ingredient(api.get_json(req)['uuid']),
  "Delete Ingredient Record"
)

API.path(
  "utensils/delete",
  lambda req, *args, **kwargs: delete_utensil(api.get_json(req)['uuid']),
  "Delete Utensil Record"
)
