# Standard library
from uuid import uuid1
# Django library
from django.db import models


class RecipeModel(models.Model):
  """
  This is the core model for recipe objects which contain data relating to
  ingredients and required tools to perform the recipe related to the record
  """
  uuid = models.CharField(
    null=False,
    blank=False,
    unique=True,
    default=uuid1,
    max_length=36,
    primary_key=True
  )
  name = models.TextField(
    null=False,
    blank=False
  )
  categories = models.TextField(
    null=False,
    blank=False,
    default=""
  )
  image = models.URLField()
  description = models.TextField(
    null=False,
    blank=False,
    default=""
  )
  prep_time = models.IntegerField()
  cook_time = models.IntegerField()
  ingredients = models.JSONField()
  utensils = models.JSONField()
  approvals = models.IntegerField()


class IngredientModel(models.Model):
  """
  This is the secondary model for recipe object which contains data relating
  to ingredients that may be required for any specific recipe
  """
  uuid = models.CharField(
    null=False,
    blank=False,
    unique=True,
    default=uuid1,
    max_length=36,
    primary_key=True
  )
  name = models.TextField(
    null=False,
    blank=False
  )
  aliases = models.TextField(
    null=False,
    blank=False,
    default=""
  )
  image = models.URLField()
  icon = models.TextField(
    null=False,
    blank=False,
    default=""
  )
  description = models.TextField(
    null=False,
    blank=False,
    default=""
  )
  types = models.TextField(
    null=False,
    blank=False,
    default=""
  )


class UtensilsModel(models.Model):
  """
  This is the secondary model for recipe object which contains data relating
  to utensils that may be required for any specific recipe
  """
  uuid = models.CharField(
    null=False,
    blank=False,
    unique=True,
    default=uuid1,
    max_length=36,
    primary_key=True
  )
  name = models.TextField(
    null=False,
    blank=False
  )
  aliases = models.TextField(
    null=False,
    blank=False,
    default=""
  )
  icon = models.TextField(
    null=False,
    blank=False,
    default=""
  )
