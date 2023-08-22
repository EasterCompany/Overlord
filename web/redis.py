import redis as __redis__
from web.settings import SECRET_DATA

host=SECRET_DATA['REDIS_HOST']
port=SECRET_DATA['REDIS_PORT']

try:
  redis = __redis__.Redis(host=host, port=port, db=0)
except:
  pass
