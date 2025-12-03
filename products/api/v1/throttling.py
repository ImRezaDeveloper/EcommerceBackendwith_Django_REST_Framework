from django.core.cache import caches
from rest_framework.throttling import AnonRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    """
        this method uses for cache rate limiting of the users
    """
    cache = caches['default']