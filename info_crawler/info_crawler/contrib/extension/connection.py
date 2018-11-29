import redis
# Default values.
REDIS_URL = None
REDIS_HOST = '192.168.0.60'
REDIS_PORT = 6379
REDIS_PASS = 'cs.Swust'
REDIS_DB = 0


def from_settings(settings):
    url = settings.get('REDIS_URL',  REDIS_URL)
    host = settings.get('REDIS_HOST', REDIS_HOST)
    port = settings.get('REDIS_PORT', REDIS_PORT)
    password = settings.get('REDIS_PASS', REDIS_PASS)
    db = settings.get('REDIS_DB', REDIS_DB)
    # REDIS_URL takes precedence over host/port specification.
    if url:
        return redis.from_url(url)
    else:
        return redis.Redis(host=host, port=port, password=password, db=db)
