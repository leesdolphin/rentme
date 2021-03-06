import math

from aioutils.celery import asyncio_task, delay_or_call
from aioutils.task_queues import SizeBoundedTaskList
from celery.utils.log import get_task_logger
from api.trademe.errors import ClassifiedExpiredError

from rentme.celery.celery_app import app
from rentme.raw.api import get_trademe_api
from rentme.raw.importer.data_migrations.listings import migrate_listing


logger = get_task_logger(__name__)


@asyncio_task(app, ignore_result=True, rate_limit='1/m')
async def load_listings(listing_ids, *, loop):
    listing_ids = set(listing_ids)
    async with SizeBoundedTaskList(10, loop=loop) as ltl, \
            get_trademe_api(loop=loop) as api:
        for listing_id in listing_ids:
            ltl.add_coro(api.detail.listing(listing_id))
        async with SizeBoundedTaskList(5, loop=loop) as ptl:
            found_listings = set()
            for listing_future in ltl.as_completed():
                try:
                    listing = await listing_future
                except ClassifiedExpiredError as c:
                    continue
                found_listings.add(listing.listing_id)
                ptl.add_coro(
                    delay_or_call(migrate_listing, listing.listing_id)
                )
            if found_listings != listing_id:
                for listing_id in (listing_ids - found_listings):
                    ptl.add_coro(
                        delay_or_call(delete_listing, listing_id)
                    )


@asyncio_task(app, ignore_result=True, rate_limit='1/m')
async def load_rental_listing_search_results(*, loop):
    return await load_search_results('rental', loop=loop)


@asyncio_task(app, ignore_result=True, rate_limit='1/m')
async def load_flatmate_listing_search_results(*, loop):
    return await load_search_results('flatmate', loop=loop)


async def load_search_results(search_api_name, *, loop):
    search_kwargs = dict(return_metadata=True, return_ads=True,
                         return_super_features=True, sort_order='ExpiryDesc',
                         rows=25, loop=loop)
    print("SSDFKSDFSKDFSD")
    async with SizeBoundedTaskList(5, loop=loop) as stl, \
            get_trademe_api(loop=loop) as api:
        print("SSDFKSDFSKDFSD")
        search_api = getattr(api.search, search_api_name)
        logger.info("Getting page %d of %s for %s",
                    1, '?', search_api_name)
        page_1_future = await stl.add_task(
            search_api(**search_kwargs, page=1))
        search_res = await page_1_future
        pages = math.ceil(search_res.total_count / search_res.page_size)
        for page_no in range(2, pages + 1):
            logger.info("Getting page %d of %d for %s",
                        page_no, pages, search_api_name)
            stl.add_coro(
                search_api(**search_kwargs, page=page_no))
        async with SizeBoundedTaskList(5, loop=loop) as ltl:
            for page_future in stl.as_completed():
                search_res = await page_future
                ltl.add_coro(delay_or_call(load_listings, [
                    listing.listing_id for listing in search_res.list.all()
                ], loop=loop))


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


@asyncio_task(app, ignore_result=True, rate_limit='5/s')
async def delete_listing(listing_id, *, loop):
    from rentme.raw.models.search import Flatmate, Property
    from rentme.raw.models.listings import ListedItemDetail

    for model in [Flatmate, Property, ListedItemDetail]:
        try:
            model.objects.get(listing_id=listing_id).delete()
        except model.DoesNotExist:
            pass
