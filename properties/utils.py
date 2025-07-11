from django.core.cache import cache
from .models import Property
import logging

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all())
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour
    return properties

def get_redis_cache_metrics():
    """
    Retrieves Redis cache hit/miss metrics and calculates the hit ratio.
    Returns a dictionary with hits, misses, and hit_ratio.
    """

    try:
        redis_client = cache.client.get_client()
        info = redis_client.info()
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else None

        metrics = {
            'hits': hits,
            'misses': misses,
            'hit_ratio': hit_ratio
        }

        logging.info(f"Redis Cache Metrics: {metrics}")
        return metrics
    except Exception as e:
        logging.error(f"Error retrieving Redis cache metrics: {e}")
        return {'hits': None, 'misses': None, 'hit_ratio': None}