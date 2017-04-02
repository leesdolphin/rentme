import asyncio
import collections
import hashlib
import pathlib
import pickle
import traceback
import urllib.parse

import aiohttp
import multidict


CacheInfo = collections.namedtuple('CacheInfo', 'hits misses attempts')


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
            # New lock every time because no locking has been requested.
            return asyncio.Lock()
        semaphore_key = '_default_'
        if self._rate_limit_by_domain:
            parsed = urllib.parse.urlparse(url)
            semaphore_key = (parsed.scheme, parsed.netloc)
        if semaphore_key not in self._locks:
            self._locks[semaphore_key] = asyncio.BoundedSemaphore(self._max_inflight_requests)
        return self._locks[semaphore_key]


class CachingClientSession(aiohttp.client.ClientSession):

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._cache_info = CacheInfo(0, 0, 0)

    @property
    def cache_info(self):
        return self._cache_info

    async def _request(self, method, url, **kwargs):
        if kwargs.pop('no_cache', False):
            return await super()._request(method, url, **kwargs)
        self._cache_info = self._cache_info._replace(attempts=self._cache_info.attempts + 1)
        try:
            cached_response = await self.get_cached_response(method, url, **kwargs)
        except:
            raise
            cached_response = None
        if cached_response is not None:
            await self.do_cache_response(cached_response, method, url, **kwargs)
            self._cache_info = self._cache_info._replace(
                hits=self._cache_info.hits + 1)
            return cached_response
        self._cache_info = self._cache_info._replace(
            misses=self._cache_info.misses + 1)
        print('Cache miss for', method, url)
        real_response = await super()._request(method, url, **kwargs)
        try:
            await self.do_cache_response(real_response, method, url, **kwargs)
        except:
            traceback.print_exc()
            raise
        return real_response

    @staticmethod
    def standardise_url(url):
        parsed = urllib.parse.urlsplit(url)
        parsed_qs = urllib.parse.urlencode(sorted(urllib.parse.parse_qsl(parsed.query)))
        parsed = parsed._replace(query=parsed_qs)
        return urllib.parse.urlunsplit(parsed)


class CachedResponse(aiohttp.client.ClientResponse):

    @classmethod
    async def from_response(cls, response):
        content = await response.read()
        return cls(response.method, response.url, content, response.cookies,
                   response.headers, response.raw_headers, response.version,
                   response.status, response.reason)

    def __init__(self, method, url, content, cookies, headers, raw_headers, version, status, reason):
        self.__setstate__({
            'content': content,
            'url': url,
            'cookies': cookies,
            'headers': headers,
            'method': method,
            'raw_headers': raw_headers,
            'version': version,
            'status': status,
            'reason': reason,
        })
        self._get_encoding()

    def __getstate__(self):
        return {
            'content': self._content,
            'url': self._url,
            'cookies': self.cookies,
            'headers': tuple(self.headers.items()),
            'method': self.method,
            'raw_headers': self.raw_headers,
            'version': self.version,
            'status': self.status,
            'reason': self.reason,
        }

    def __setstate__(self, state):
        self._closed = True
        self._connection = None
        self._content = state['content']
        self._continue = None
        self._history = ()
        self._loop = asyncio.get_event_loop()
        self._reader = None
        self._should_close = True
        self._timeout = 0
        self._url = state['url']
        self._writer = None
        self.content = None
        self.cookies = state['cookies']
        self.headers = multidict.MultiDict(state['headers'])
        self.method = state['method']
        self.raw_headers = state['raw_headers']
        self.version = state['version']
        self.status = state['status']
        self.reason = state['reason']

    async def read(self):
        return self._content


class OnDiskCachingClientSession(CachingClientSession):

    def __init__(self, *a, cache_folder, **k):
        self.cache_folder = pathlib.Path(cache_folder).resolve()
        self.cache_folder.mkdir(exist_ok=True)
        super().__init__(*a, **k)

    def _get_filename(self, method, url, **kwargs):
        key = hashlib.sha512()
        key.update(method.encode())
        key.update(self.standardise_url(url).encode())
        key.update(repr(sorted(kwargs.items())).encode())
        file = self.cache_folder / (key.hexdigest() + '.pickle')
        return file

    async def get_cached_response(self, method, url, **kwargs):
        filename = self._get_filename(method, url, **kwargs)
        try:
            with filename.open('rb') as f:
                unpickled = pickle.load(f)
            try:
                await unpickled.text()
                return unpickled
            except:
                filename.unlink()
                raise
        except (IOError, EOFError, ImportError):
            return None

    async def do_cache_response(self, response, method, url, **kwargs):
        filename = self._get_filename(method, url, **kwargs)
        response = await CachedResponse.from_response(response)
        with filename.open('wb') as f:
            pickle.dump(response, f)
        try:
            loaded_resp = await self.get_cached_response(method, url, **kwargs)
            await loaded_resp.json()
        except:
            filename.unlink()
            raise
