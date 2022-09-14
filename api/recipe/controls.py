# Standard library
import json
# Overlord library
from core.library import api
from api.recipe.tables import *


def list_all_recipes():
  """
  Returns a list of all recipe objects within the database
  """

  def __body__(body_query):
    body_row_data = []
    for recipe in body_query:
      body_row_data.append([
        recipe.uuid,
        recipe.name,
        recipe.categories,
        recipe.description,
        recipe.prep_time,
        recipe.cook_time,
        recipe.approvals
      ])
    return body_row_data

  return api.table(
    Table=RecipeModel,
    Headers=['UUID', 'Name', 'Categories', 'Description', 'Prep Time', 'Cook Time', 'Approvals'],
    Body=__body__,
    filter={ "order_by": "name" }
  )


def list_all_ingredients():
  """
  Returns a list of all ingredient records within the database
  """

  def __body__(body_query):
    body_row_data = []
    for ing in body_query:
      body_row_data.append([
        ing.uuid,
        ing.name,
        ing.aliases,
        ing.description,
        ing.types
      ])
    return body_row_data

  return api.table(
    Table=IngredientModel,
    Headers=['UUID', 'Name', 'Aliases', 'Description', 'Types'],
    Body=__body__,
    filter={ "order_by": "name" }
  )


# --- UTENSILS ---
def list_all_utensils():
  """
  Returns a list of all ingredient records within the database
  """

  def __body__(body_query):
    body_row_data = []
    for utl in body_query:
      body_row_data.append([
        utl.uuid,
        utl.name,
        utl.aliases
      ])
    return body_row_data

  return api.table(
    Table=UtensilsModel,
    Headers=['UUID', 'Name', 'Aliases'],
    Body=__body__,
    filter={ "order_by": "name" }
  )


def create_new_utensils(req):
  data = api.get_json(req)
  try:
    UtensilsModel.objects.create(
      name=data['name'],
      aliases=data['aliases'],
      icon=data['icon']
    )
  except Exception as error:
    return api.error(error)
  return api.success()
