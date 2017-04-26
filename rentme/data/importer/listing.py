import asyncio
import math

from celery.utils.log import get_task_logger
from trademe.errors import ClassifiedExpiredError

from rentme.data.importer.celery import app
from rentme.data.importer.utils import asyncio_task, get_trademe_api


logger = get_task_logger(__name__)


@asyncio_task(app, ignore_result=True, rate_limit='1/s')
async def load_listing(listing_id, *, _loop):
    try:
        async with get_trademe_api() as api:
            await api.listing.listing(listing_id)
    except ClassifiedExpiredError as e:
        pass


@asyncio_task(app, ignore_result=True)
async def load_listing_search_results(*, _loop):
    search_kwargs = dict(return_metadata=True, return_ads=True,
                         return_super_features=True, sort_order='ExpiryDesc',
                         rows=25)
    async with get_trademe_api() as api:
        page_1_future = asyncio.ensure_future(
            api.search.rental(**search_kwargs, page=1),
            loop=_loop)
        search_res = await page_1_future
        pages = math.ceil(search_res.total_count / search_res.page_size)
        pages_futures = [page_1_future]
        for page_no in range(2, pages + 1):
            pages_futures.append(asyncio.ensure_future(
                api.search.rental(**search_kwargs, page=1),
                loop=_loop))
        for page_future in asyncio.as_completed(pages_futures, loop=_loop):
            search_res = await page_future
            for listing_id in search_res.list:
                load_listing.delay(listing_id)
