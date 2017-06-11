from .rate_limit import RateLimitingSession
from .cache import CachingClientSession, CachingStrategy, OnDiskCachingStrategy
from .cache import MigratingCachingStrategy


class RateLimitingCachingClientSession(
        RateLimitingSession, CachingClientSession):
    pass


__all__ = (
    'CachingClientSession',
    'CachingStrategy',
    'MigratingCachingStrategy',
    'OnDiskCachingStrategy',
    'RateLimitingCachingClientSession',
    'RateLimitingSession',
)
