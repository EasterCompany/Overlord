# Standard library
import secrets
from uuid import uuid1
# Django library
from django.db import models


class AdminPanel(models.Model):
  """
  This model is the base model for an admin panel (e-panel) which controls
  which users can access a panel and what capabilities each panel has
  """
  uuid = models.CharField(
    null=False,
    blank=False,
    unique=True,
    default=uuid1,
    max_length=36,
    primary_key=True
  )
  secret_key = models.TextField(
    null=False,
    blank=False,
    default=secrets.token_urlsafe
  )
  name = models.TextField(
    null=False,
    blank=False
  )
  api = models.TextField(
    null=False,
    blank=False
  )
  users = models.JSONField(
    null=False,
    blank=False
  )
  create_cmd = models.TextField(
    null=False,
    blank=False,
    default=""
  )
  install_cmd = models.TextField(
    null=False,
    blank=False,
    default=""
  )
  run_cmd = models.TextField(
    null=False,
    blank=False,
    default=""
  )
  description = models.TextField(
    null=False,
    blank=False,
    default=""
  )
