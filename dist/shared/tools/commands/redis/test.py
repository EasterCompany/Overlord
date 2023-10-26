import redis
from core.library import console
from web.settings import SECRET_DATA


def run() -> str|None:
  console.out("\n> Fetching Secret Data")
  if not 'REDIS_HOST' in SECRET_DATA:
    return console.out(f"  {console.failure} REDIS_HOST in '.config/secret.json' not set", "red")
  else:
    console.out(f"  {console.success} REDIS_HOST set", "success")
  if not 'REDIS_PORT' in SECRET_DATA:
    return console.out(f"  {console.failure} REDIS_PORT in '.config/secret.json' not set", "red")
  else:
    console.out(f"  {console.success} REDIS_PORT set", "success")

  console.out("\n> Starting Redis DB")
  r = redis.Redis(host=SECRET_DATA['REDIS_HOST'], port=SECRET_DATA['REDIS_PORT'], db=0)
  console.out(f"  {console.success} Success", "success")

  console.out("\n> Setting 'foo' to 'bar'")
  setter = r.set('foo', 'bar')
  if not setter:
    return console.out(f"  {console.failure} Failed", "red")
  else:
    console.out(f"  {console.success} Success", "success")

  console.out("\n> Getting 'foo'")
  getter = r.get('foo')
  if not getter == b'bar':
    return console.out(f"  {console.failure} Failed", "red")
  else:
    console.out(f"  {console.success} Success", "success")
