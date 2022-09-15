# Standard library
from uuid import uuid1
# Overlord library
from core.library import models


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
  images = models.TextField(
    null=False,
    blank=False,
    default=""
  )
  description = models.TextField(
    null=False,
    blank=False,
    default=""
  )
  prep_time = models.IntegerField()
  cook_time = models.IntegerField()
  ingredients = models.JSONField()
  utensils = models.JSONField()
  approvals = models.IntegerField(
    null=True,
    blank=False,
    default=0
  )


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
  image = models.TextField()
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


class UtensilModel(models.Model):
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

  def __str__(self, *args, **kwargs):
    return str(self.uuid)
