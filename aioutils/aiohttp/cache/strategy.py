from abc import ABCMeta, abstractmethod
import base64
import hashlib
import pathlib
import pickle

from .session import CachedResponse
from .filter import CacheFilter

def b64encode(byte_str):
    return base64.b64encode(byte_str).decode()


class CachingStrategy(metaclass=ABCMeta):

    @abstractmethod
    async def get_cached_response(self, method, url, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def do_cache_response(self, response, method, url, **kwargs):
        raise NotImplementedError()

    def sanitise_arguments(self, method, url, cache_filter=None, **kwargs):
        if not cache_filter:
            cache_filter = CacheFilter()
        method, url, kwargs = cache_filter.filter(method, url, kwargs)
        return method, url, kwargs


class OnDiskCachingStrategy(CachingStrategy):

    def __init__(self, *a, cache_folder, **k):
        self.cache_folder = pathlib.Path(cache_folder).resolve()
        self.cache_folder.mkdir(exist_ok=True)
        super().__init__(*a, **k)

    def _get_filename(self, method, url, **kwargs):
        method, url, kwargs = self.sanitise_arguments(method, url, **kwargs)
        key = hashlib.sha512()
        key.update(method.encode())
        key.update(self.standardise_url(url).encode())
        key.update(repr(kwargs.items()).encode())
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
