import asyncio
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import functools
import http.cookies
import json
import uuid
import logging

from aioutils import asyncio_loop
from celery import Celery
from celery.local import PromiseProxy
from celery.utils.log import get_task_logger
from django.db import connections
from django.utils import timezone
from trademe.api import RootManager
from trademe.cache import CachedResponse, CachingClientSession, CachingStrategy
from trademe.cache import RateLimitingCachingClientSession

from rentme.data.importer.models import CachedResponse as CachedResponseModel
# from rentme.data.models.registry import model_registry

logger = get_task_logger(__name__)


def b64encode(byte_str):
    return base64.b64encode(byte_str).decode()


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
        new_loop.set_debug(True)
        logging.getLogger('asyncio').setLevel(logging.DEBUG)
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
                    logger.error('Not Done Tasks %r', [task for task in asyncio.Task.all_tasks(new_loop) if not task.done()])
                    ex = TypeError('Function did not clean up tasks.')
                new_loop.close()
                del new_loop
                if ex:
                    raise ex

    return wrapper


def asyncio_task(app, **kwargs):
    assert isinstance(app, Celery)
    kwargs.setdefault('track_started', True)

    def wrapper(fn):
        task = app.task(**kwargs)(wrap_async_fn_in_new_event_loop(fn))
        return AsyncioPromiseProxy(task, fn, __doc__=fn.__doc__)

    return wrapper


@asyncio_loop
def get_trademe_session(loop=None, rate_limit=False):
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
    if rate_limit:
        if rate_limit is True:
            rate_limit = 5
        return RateLimitingCachingClientSession(
            max_inflight_requests=rate_limit, rate_limit_by_domain=True,
            cache_strategy=DatabaseCachingStrategy(), loop=loop,
            cookies=cookies, headers=headers
        )
    else:
        return CachingClientSession(
            cache_strategy=DatabaseCachingStrategy(), loop=loop,
            cookies=cookies, headers=headers)


def get_trademe_api(session=None, db_models=True, _loop=None):
    if session is None:
        session = get_trademe_session(_loop=_loop)
    if db_models:
        return RootManager(
            session,
            # model_registry=model_registry
        )
    else:
        return RootManager(session)


class InMemoryCachingStrategy(CachingStrategy):

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


class DatabaseCachingStrategy(CachingStrategy):

    def __init__(self, *a, expiry_time=timedelta(days=7), **k):
        super().__init__(*a, **k)
        if isinstance(expiry_time, timedelta):
            self._expiry_time = expiry_time
        else:
            self._expiry_time = timedelta(seconds=expiry_time)

    def get_cache_key(self, method, url, **kwargs):
        return method, self.standardise_url(url), json.dumps(sorted(kwargs.items()))

    @asyncio_loop
    async def get_cached_response(self, method, url, *, loop, **kwargs):
        return await loop.run_in_executor(
            None, self.get_cached_response_sync,
            loop, method, url, kwargs)

    def get_cached_response_sync(self, loop, method, url, kwargs):
        method, url, kwargs = self.get_cache_key(method, url, **kwargs)
        try:
            model = CachedResponseModel.objects.get(
                method=method,
                url=url,
                kwargs=kwargs,
                expiry__gte=timezone.now()
            )
            content = model.content.tobytes()
            response_state = json.loads(model.data)
            response_state['loop'] = loop
            return CachedResponse.from_json_dict(response_state, content=content)
        except CachedResponseModel.DoesNotExist:
            return None

    @asyncio_loop
    async def do_cache_response(self, response, method, url, *, loop, **kwargs):
        response = await CachedResponse.from_response(response)
        return await loop.run_in_executor(
            None, self.do_cache_response_sync,
            response, method, url, kwargs)

    def do_cache_response_sync(self, cached_response, method, url, kwargs):
        method, url, kwargs = self.get_cache_key(method, url, **kwargs)
        state = cached_response.to_json_dict(encode_content=False)

        content = state.pop('content')
        data = json.dumps(state)
        expiry = timezone.now() + self._expiry_time
        model, _ = CachedResponseModel.objects.update_or_create(
            method=method,
            url=url,
            kwargs=kwargs,
            defaults=dict(
                content=content,
                data=data,
                expiry=expiry,
            )
        )
        model.save()
