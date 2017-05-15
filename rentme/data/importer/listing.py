import asyncio
import math

from celery.utils.log import get_task_logger
from django.utils import timezone
from trademe.errors import ClassifiedExpiredError

from rentme.data.importer.celery import app
from rentme.data.importer.cleanup import clean_related_tables
from rentme.data.importer.utils import asyncio_task
from rentme.data.importer.utils import get_trademe_api, get_trademe_session
from rentme.data.models.listing import Listing

logger = get_task_logger(__name__)


@asyncio_task(app, ignore_result=True, rate_limit='5/m')
async def load_listing(listing_id, *, _loop):
    async with get_trademe_api(_loop=_loop) as api:
        try:
            await api.listing.listing(listing_id)
        except ClassifiedExpiredError as e:
            try:
                Listing.objects.get(listing_id=listing_id).delete()
            except Listing.DoesNotExist:
                pass


@asyncio_task(app, ignore_result=True, rate_limit='1/s')
async def load_listings(listing_ids, *, _loop):
    async with get_trademe_api(_loop=_loop) as api:
        listing_futures = {}
        for listing_id in listing_ids:
            listing_futures[listing_id] = asyncio.ensure_future(
                api.listing.listing(listing_id),
                loop=_loop)
        for listing_id, listing_fut in listing_futures:
            try:
                await listing_fut
            except ClassifiedExpiredError as e:
                try:
                    Listing.objects.get(listing_id=listing_id).delete()
                except Listing.DoesNotExist:
                    pass


@asyncio_task(app, ignore_result=True)
async def load_listing_search_results(*, _loop):
    search_kwargs = dict(return_metadata=True, return_ads=True,
                         return_super_features=True, sort_order='ExpiryDesc',
                         rows=25)
    async with get_trademe_api(_loop=_loop) as api:
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
        listings = []
        for page_future in asyncio.as_completed(pages_futures, loop=_loop):
            search_res = await page_future
            for listing_id in search_res.list:
                listings.append(listing_id)
            if len(listings) > 100:
                load_listings.delay(listings)
                listings = []
        if listings:
            load_listings.delay(listings)


async def delete_if_missing(session, api, listing):
    url = ('http://www.trademe.co.nz/property/residential-property-to-rent/'
           'auction-%s.htm' % (listing.listing_id, ))
    async with session.head(url, no_cache=True) as response:
        if response.status == 200:
            # Listing still exists
            try:
                await api.listing.listing(listing.listing_id)
            except ClassifiedExpiredError:
                listing.delete()
        else:
            listing.delete()


@asyncio_task(app, ignore_result=True)
async def delete_all_outdated(*, _loop):
    async with get_trademe_session(_loop=_loop, rate_limit=True) as session, \
            get_trademe_api(session=session, _loop=_loop) as api:
        missing_futures = []
        for listing in Listing.objects.filter(end_date__lt=timezone.now()):
            missing_futures.append(delete_if_missing(session, api, listing))
        gather = asyncio.ensure_future(asyncio.gather(*missing_futures, loop=_loop), loop=_loop)
        try:
            await gather
        except:
            gather.cancel()
            raise
    clean_related_tables.delay()
