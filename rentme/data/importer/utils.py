import asyncio
from concurrent.futures import ThreadPoolExecutor
import functools
import uuid

from celery.local import PromiseProxy
from celery.utils.log import get_task_logger
from django.db import connections
from trademe.api import RootManager
from trademe.cache import CachedResponse, CachingClientSession

from rentme.data.models.registry import model_registry


logger = get_task_logger(__name__)


class AsyncioPromiseProxy(PromiseProxy):

    __slots__ = ('__original_fn')

    def __init__(self, proxy, original_fn, name=None, __doc__=None):
        super().__init__(lambda: proxy, (), {},
                         name=name, __doc__=__doc__)
        object.__setattr__(self, '_AsyncioPromiseProxy__original_fn', original_fn)

    def __call__(self, *a, **k):
        k.setdefault('_loop', asyncio.get_event_loop())
        return self.__original_fn(*a, **k)


def wrap_async_fn_in_new_event_loop(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        new_loop = asyncio.new_event_loop()
        with ThreadPoolExecutor(max_workers=2) as executor:
            new_loop.set_default_executor(executor)
            try:
                # asyncio.set_event_loop(new_loop)
                result = fn(*args, _loop=new_loop, **kwargs)
                return new_loop.run_until_complete(result)
            finally:
                # Try and force all connections to close themselves.
                connections.close_all()
                for _ in range(executor._max_workers * 2):
                    executor.submit(connections.close_all)
                # asyncio.set_event_loop(old_loop)
                ex = None
                if any(map(lambda task: not task.done(),
                           asyncio.Task.all_tasks(new_loop))):
                    ex = TypeError('Function did not clean up tasks.')
                new_loop.close()
                del new_loop
                if ex:
                    raise ex

    return wrapper


def asyncio_task(app, **kwargs):
    kwargs.setdefault('track_started', True)

    def wrapper(fn):
        task = app.task(**kwargs)(wrap_async_fn_in_new_event_loop(fn))
        return AsyncioPromiseProxy(task, fn, __doc__=fn.__doc__)

    return wrapper


def get_trademe_session(_loop=None):
    tm_uid = 'goldilocks-' + str(uuid.uuid4())
    cookies = {'x-trademe-uniqueclientid:': tm_uid}

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0)'
                      ' Gecko/20100101 Firefox/50.0',
        'Referer': 'https://preview.trademe.co.nz/property/trade-me-property'
                   '/residential-to-rent/1243057304',
        'Cache-Control': 'no-cache',
        'x-trademe-uniqueclientid': tm_uid,
    }

    return InMemoryCachingClientSession(loop=_loop, cookies=cookies, headers=headers)


def get_trademe_api(session=None, db_models=True, _loop=None):
    if session is None:
        session = get_trademe_session(_loop=_loop)
    if db_models:
        return RootManager(session, model_registry=model_registry)
    else:
        return RootManager(session)


class InMemoryCachingClientSession(CachingClientSession):

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._cache = {}

    def get_cache_key(self, method, url, **kwargs):
        return method, self.standardise_url(url), frozenset(kwargs.items())

    async def get_cached_response(self, method, url, **kwargs):
        key = self.get_cache_key(method, url, **kwargs)
        return self._cache.get(key, None)

    async def do_cache_response(self, response, method, url, **kwargs):
        key = self.get_cache_key(method, url, **kwargs)
        response = await CachedResponse.from_response(response)
        self._cache[key] = response
