import redis as __redis__
from shared import settings as __settings__

dump = __redis__.Redis(
  host=__settings__.redis_host,
  port=__settings__.redis_port + 0,
  db=__settings__.redis_port + 0
)

active_sessions = __redis__.Redis(
  host=__settings__.redis_host,
  port=__settings__.redis_port + 1,
  db=__settings__.redis_port + 1
)

rdfs = __redis__.Redis(
  host=__settings__.redis_host,
  port=__settings__.redis_port + 2,
  db=__settings__.redis_port + 2
)
