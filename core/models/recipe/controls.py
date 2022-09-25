# Overlord library
from core.library import api
from core.models.recipe.tables import *


# --- RECIPES ---
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


def create_new_recipe(req):
  data = api.get_json(req)
  try:
    RecipeModel.objects.create(
      name=data['name'],
      categories=data['categories'],
      images=data['images'],
      description=data['description'],
      prep_time=int(data['prep_time']),
      cook_time=int(data['cook_time']),
      ingredients=data['ingredients'],
      utensils=data['utensils']
    )
  except Exception as error:
    api.error(error)
  return api.success()


def delete_recipe(uuid):
  """
  Deletes an existing recipe record
  """
  try:
    RecipeModel.objects.get(uuid=uuid.strip()).delete()
  except Exception as error:
    return api.error(error)
  return api.success()


# --- INGREDIENTS ---
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


def create_new_ingredient(req):
  """
  Creates a new database record for the ingredients model
  """
  data = api.get_json(req)
  try:
    IngredientModel.objects.create(
      name=data['name'],
      aliases=data['aliases'],
      image=data['image'],
      icon=data['icon'],
      description=data['description'],
      types=data['types']
    )
  except Exception as error:
    return api.error(error)
  return api.success()


def delete_ingredient(uuid):
  """
  Deletes an existing ingredient record
  """
  try:
    IngredientModel.objects.get(uuid=uuid.strip()).delete()
  except Exception as error:
    return api.error(error)
  return api.success()


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
    Table=UtensilModel,
    Headers=['UUID', 'Name', 'Aliases'],
    Body=__body__,
    filter={ "order_by": "name" }
  )


def create_new_utensil(req):
  """
  Creates a new record for the utensils model
  """
  data = api.get_json(req)
  try:
    UtensilModel.objects.create(
      name=data['name'],
      aliases=data['aliases'],
      icon=data['icon']
    )
  except Exception as error:
    return api.error(error)
  return api.success()


def delete_utensil(uuid):
  """
  Deletes an existing utensil record
  """
  try:
    UtensilModel.objects.get(uuid=uuid.strip()).delete()
  except Exception as error:
    return api.error(error)
  return api.success()


# --- FOREIGN KEYS ---
def list_foreign_keys():
  """
  Returns ingredient & utensil data so the recipe view can link to these records
  :return: { status: <str>, data: { utensils: <list>, ingredients: <list> } }
  """
  try:
    utensils = UtensilModel.objects.all()
    ingredients = IngredientModel.objects.all()
    return api.data({
      'utensils': [
        {
          'uuid': utensil.uuid,
          'icon': utensil.icon,
          'name': utensil.name,
          'aliases': utensil.aliases
        } for utensil in utensils.iterator()
      ],
      'ingredients': [
        {
          'uuid': i.uuid,
          'icon': i.icon,
          'name': i.name,
          'aliases': i.aliases
        } for i in ingredients.iterator()
      ]
    })
  except Exception as error:
    api.error(error)
  return api.success()
