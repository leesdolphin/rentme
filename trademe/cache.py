import asyncio
import base64
import collections
import hashlib
import http.cookies
import pathlib
import pickle
import urllib.parse

import aiohttp
import aiohttp.http_writer
import aioutils.aiohttp
import multidict
import yarl


def b64encode(byte_str):
    return base64.b64encode(byte_str).decode()


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
        data['cookies'] = http.cookies.SimpleCookie('\r\n'.join(data['cookies']))

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

    async def _request(self, method, url, **kwargs):
        if kwargs.pop('no_cache', False):
            return await super()._request(method, url, **kwargs)
        self._cache_info = self._cache_info._increment(attempts=1)

        cached_response = await self._cache_strategy.get_cached_response(
            method, url, **kwargs)
        if cached_response is not None:
            self._cache_info = self._cache_info._increment(hits=1)
            return cached_response

        self._cache_info = self._cache_info._increment(misses=1)
        print('Cache miss for', method, url)
        real_response = await super()._request(method, url, **kwargs)
        await self._cache_strategy.do_cache_response(real_response, method, url, **kwargs)

        return real_response


class RateLimitingCachingClientSession(
        aioutils.aiohttp.RateLimitingSession,
        CachingClientSession):
    pass


class CachingStrategy(object):

    @staticmethod
    def standardise_url(url):
        parsed = urllib.parse.urlsplit(url)
        parsed_qs = urllib.parse.urlencode(sorted(urllib.parse.parse_qsl(parsed.query)))
        parsed = parsed._replace(query=parsed_qs)
        return urllib.parse.urlunsplit(parsed)

    async def get_cached_response(self, method, url, **kwargs):
        raise NotImplementedError()

    async def do_cache_response(self, response, method, url, **kwargs):
        raise NotImplementedError()


class OnDiskCachingStrategy(CachingStrategy):

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


class MigratingCachingStrategy(CachingStrategy):

    def __init__(self, *a, primary_cache, old_caches=(), **k):
        super().__init__(*a, **k)
        self.primary_cache = primary_cache
        self.old_caches = tuple(old_caches)

    async def get_cached_response(self, method, url, **kwargs):
        primary_response = await self.primary_cache.get_cached_response(
            method, url, **kwargs)
        if primary_response is not None:
            return primary_response
        for cache in self.old_caches:
            cache_response = await cache.get_cached_response(
                method, url, **kwargs)
            if cache_response is not None:
                await self.do_cache_response(
                    cache_response, method, url, **kwargs)
                return cache_response
        return None

    async def do_cache_response(self, response, method, url, **kwargs):
        await self.primary_cache.do_cache_response(
            response, method, url, **kwargs)
