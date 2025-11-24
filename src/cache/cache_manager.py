import requests_cache
import datetime

def install_cache():
    """
    Installs a global cache for requests.
    Cache expires after 1 day.
    """
    requests_cache.install_cache(
        'geo_cache',
        backend='sqlite',
        expire_after=datetime.timedelta(days=1)
    )

def get_session():
    """
    Returns a cached session.
    """
    session = requests_cache.CachedSession(
        'geo_cache',
        backend='sqlite',
        expire_after=datetime.timedelta(days=1)
    )
    return session
