from time import time

_cache={}

CACHE_TTL=300 #5 minutes

def get_cached_response(key:str):
    """
    Return cached response if it exists and has not expired.
    """

    cached=_cache.get(key)

    if cached is None:
        return None

    response,timestamp=cached

    if time()- timestamp>CACHE_TTL:
        del _cache[key]
        return None

    return response

def set_cached_response(key:str,response:str):
    """
    Store an AI response in the cache.
    """

    _cache[key]=(
        response,
        time()
    )

