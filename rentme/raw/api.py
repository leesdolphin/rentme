import base64
from datetime import timedelta
import json
import uuid

from celery.utils.log import get_task_logger
from django.utils import timezone

from aioutils import asyncio_loop
from aioutils.aiohttp.cache import CachingClientSession, CachingStrategy
from aioutils.aiohttp.cache import RateLimitingCachingClientSession
from aioutils.aiohttp.cache.session import CachedResponse
from api.trademe import RootManager

from rentme.raw.importer.models import CachedResponse as CachedResponseModel
from rentme.data.models import create_discoverer as create_data_discoverer
from rentme.raw.models import create_discoverer as create_raw_discoverer
from rentme.raw.loader import Deserializer, MutliDiscoverer

logger = get_task_logger(__name__)


def b64encode(byte_str):
    return base64.b64encode(byte_str).decode()


@asyncio_loop
def get_trademe_session(loop=None, rate_limit=True):
    # tm_uid = 'goldilocks-' + str(uuid.uuid4())
    # cookies = {'x-trademe-uniqueclientid:': tm_uid}
    #
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0)'
    #                   ' Gecko/20100101 Firefox/50.0',
    #     'Referer': 'https://preview.trademe.co.nz/property/trade-me-property'
    #                '/residential-to-rent/123456789',
    #     'Cache-Control': 'no-cache',
    #     'x-trademe-uniqueclientid': tm_uid,
    # }
    if rate_limit:
        if rate_limit is True:
            rate_limit = 5
        return RateLimitingCachingClientSession(
            max_inflight_requests=rate_limit, rate_limit_by_domain=True,
            cache_strategy=DatabaseCachingStrategy(), loop=loop,
            # cookies=cookies, headers=headers
        )
    else:
        return CachingClientSession(
            cache_strategy=DatabaseCachingStrategy(), loop=loop,
            # cookies=cookies, headers=headers
        )


def get_trademe_api(session=None, loop=None):
    if session is None:
        session = get_trademe_session(loop=loop)
    deserializer = Deserializer(MutliDiscoverer(
        create_raw_discoverer(),
        create_data_discoverer(),
    ))
    return RootManager(session, deserializer=deserializer)


class DatabaseCachingStrategy(CachingStrategy):

    def __init__(self, *a, expiry_time=timedelta(days=7), **k):
        super().__init__(*a, **k)
        if isinstance(expiry_time, timedelta):
            self._expiry_time = expiry_time
        else:
            self._expiry_time = timedelta(seconds=expiry_time)

    def get_cache_key(self, method, url, **kwargs):
        method, url, kwargs = self.sanitise_arguments(method, url, **kwargs)
        return (method, url, json.dumps(list(kwargs.items())))

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
            return CachedResponse.from_json_dict(response_state,
                                                 content=content)
        except CachedResponseModel.DoesNotExist:
            return None

    @asyncio_loop
    async def do_cache_response(self, response, method, url, *,
                                loop, **kwargs):
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
