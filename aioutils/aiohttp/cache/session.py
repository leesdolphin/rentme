import asyncio
import base64
import collections
import http.cookies

import aiohttp
import aiohttp.http_writer
import multidict
import yarl

from ..rate_limit import RateLimitingSession


class CacheInfo(collections.namedtuple('CacheInfo', 'hits misses attempts')):

    __slots__ = ()

    def _increment(self, hits=0, misses=0, attempts=0):
        return self._replace(
            hits=self.hits + hits,
            misses=self.misses + misses,
            attempts=self.attempts + attempts)


class CachedResponse(aiohttp.client.ClientResponse):

    @classmethod
    async def from_response(cls, response):
        content = await response.read()
        return cls(response.method, response.url, content, response.cookies,
                   response.headers, response.raw_headers, response.version,
                   response.status, response.reason)

    @classmethod
    def from_json_dict(cls, data, *, content=None):
        if content is None:
            data['content'] = base64.b64decode(data['content'])
        else:
            data['content'] = content
        data['raw_headers'] = tuple(
            (base64.b64decode(key), base64.b64decode(value))
            for key, value in data['raw_headers']
        )
        data['cookies'] = http.cookies.SimpleCookie(
            '\r\n'.join(data['cookies'])
        )

        return cls(**data)

    def __init__(self, method, url, content, cookies, headers, raw_headers,
                 version, status, reason, loop=None):
        self.__setstate__({
            'content': content,
            'url': url,
            'cookies': cookies,
            'headers': headers,
            'method': method,
            'raw_headers': raw_headers,
            'version': tuple(version),
            'status': status,
            'reason': reason,
            'loop': loop
        })
        self._get_encoding()

    def __getstate__(self):
        return {
            'content': self._content,
            'url': str(self._url),
            'cookies': self.cookies,
            'headers': tuple(self.headers.items()),
            'method': self.method,
            'raw_headers': self.raw_headers,
            'version': tuple(self.version),
            'status': self.status,
            'reason': self.reason,
        }

    def __setstate__(self, state):
        self._closed = True
        self._connection = None
        self._content = state['content']
        self._continue = None
        self._history = ()
        self._loop = state.get('loop') or asyncio.get_event_loop()
        self._reader = None
        self._should_close = True
        self._timeout = 0
        self._url = yarl.URL(state['url'])
        self._writer = None
        self.content = None
        self.cookies = state['cookies']
        self.headers = multidict.MultiDict(state['headers'])
        self.method = state['method']
        self.raw_headers = state['raw_headers']
        self.version = aiohttp.http_writer.HttpVersion(*state['version'])
        self.status = state['status']
        self.reason = state['reason']

    def to_json_dict(self, encode_content=True):
        data = self.__getstate__()
        if encode_content:
            data['content'] = base64.b64encode(data['content']).decode()
        data['raw_headers'] = tuple(
            (base64.b64encode(key).decode(), base64.b64encode(value).decode())
            for key, value in data['raw_headers']
        )
        data['cookies'] = tuple(
            cookie.OutputString()
            for cookie in data['cookies'].values()
        )
        return data

    async def read(self):
        return self._content


class CachingClientSession(aiohttp.client.ClientSession):

    def __init__(self, *a, cache_strategy, **k):
        super().__init__(*a, **k)
        self._cache_strategy = cache_strategy
        self._cache_info = CacheInfo(0, 0, 0)

    @property
    def cache_info(self):
        return self._cache_info

    async def _request(self, method, url, *,
                       cache_filter=None, no_cache=False, **kwargs):
        if no_cache:
            return await super()._request(method, url, **kwargs)
        self._cache_info = self._cache_info._increment(attempts=1)
        cached_response = await self._cache_strategy.get_cached_response(
            method, url, cache_filter=cache_filter, **kwargs)
        if cached_response is not None:
            self._cache_info = self._cache_info._increment(hits=1)
            return cached_response

        self._cache_info = self._cache_info._increment(misses=1)
        print('Cache miss for', method, url)
        real_response = await super()._request(method, url, **kwargs)
        await self._cache_strategy.do_cache_response(
            real_response, method, url, cache_filter=cache_filter, **kwargs
        )
        return real_response


class RateLimitingCachingClientSession(
        RateLimitingSession,
        CachingClientSession):

    def __init__(self, *a, cache_miss_delay=10, **k):
        super().__init__(*a, **k)
        self.cache_miss_delay = float(cache_miss_delay)
        assert self.cache_miss_delay > 0

    async def _locked_request(self, *a, **k):
        response = None
        try:
            response = await super()._locked_request(*a, **k)
            return response
        finally:
            if not isinstance(response, CachedResponse):
                await asyncio.sleep(self.cache_miss_delay)
