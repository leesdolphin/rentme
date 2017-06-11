import asyncio
import urllib.parse

import aiohttp


class RateLimitingSession(aiohttp.client.ClientSession):

    def __init__(self, *a,
                 max_inflight_requests=None, rate_limit_by_domain=False, **k):
        super().__init__(*a, **k)
        assert max_inflight_requests is None or max_inflight_requests > 0
        self._max_inflight_requests = max_inflight_requests
        self._rate_limit_by_domain = rate_limit_by_domain
        self._locks = dict()

    async def _request(self, method, url, **kwargs):
        if self._max_inflight_requests is None:
            return await super()._request(method, url, **kwargs)
        async with self.request_lock(url):
            return await super()._request(method, url, **kwargs)

    def request_lock(self, url):
        if self._max_inflight_requests is None:
            raise Exception('Cannot create a lock when locking is disabled.')
        semaphore_key = '_default_'
        if self._rate_limit_by_domain:
            parsed = urllib.parse.urlparse(url)
            semaphore_key = (parsed.scheme, parsed.netloc)
        if semaphore_key not in self._locks:
            self._locks[semaphore_key] = asyncio.BoundedSemaphore(self._max_inflight_requests)
        return self._locks[semaphore_key]
