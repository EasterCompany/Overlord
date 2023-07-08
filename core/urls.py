#  core/models.py
#    automatically generated file
#    do not modify or remove

# Overlord library
from core.library import path
from core.tools.commands.external import external_command

URLS = [
  path(
    "api/o-core/external-command",
    external_command,
    name="Endpoint for remotely interfacing with the Overlord instance on this machine."
  )
]
