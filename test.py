import asyncio
from datetime import datetime, timezone
import logging
import os
import traceback
import uuid
from pprint import pprint
import warnings

from aioutils.aiohttp import RateLimitingSession
from aioutils.task_queues import AsyncTaskTracker
import django


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentme.settings')
    django.setup()

loop = asyncio.get_event_loop()

SCRIPT_DIR = os.path.dirname(__file__)


async def load_search_results():
    from rentme.raw.importer import listing
    await asyncio.gather(
        listing.load_flatmate_listing_search_results(),
        listing.load_rental_listing_search_results(),
    )


async def reload_catalogue():
    from rentme.raw.importer import catalogue
    await asyncio.gather(
        catalogue.reload_categories(),
        catalogue.reload_localities(),
        catalogue.reload_membership_localities(),
    )


async def reload_listings():
    from rentme.raw.importer.listing import delete_listing
    from aioutils.task_queues import SizeBoundedTaskList
    from rentme.raw.api import get_trademe_api
    from rentme.raw.models import listings, search

    async def get_listing(api, listing_id):
        try:
            return await api.detail.listing(listing_id)
        except:
            await delete_listing(listing_id)

    # await load_rental_listing_search_results()
    # await load_flatmate_listing_search_results()
    async with SizeBoundedTaskList(5, loop=loop) as ltl, \
            get_trademe_api(loop=loop) as api:
        all_listings = set()
        for listing in search.Flatmate.objects.all():
            all_listings.add(listing.listing_id)
        for listing in search.Property.objects.all():
            all_listings.add(listing.listing_id)
        for listing in listings.ListedItemDetail.objects.all():
            all_listings.discard(listing.listing_id)
        for listing_id in all_listings:
            ltl.add_coro(get_listing(api, listing_id))
        for idx, lstng in enumerate(ltl.as_completed()):
            print("{: >6d}/{: <6d}".format(idx, len(all_listings)))
            try:
                await lstng
            except:
                pass


async def try_insights():
    from aioutils.task_queues import SizeBoundedTaskList
    from rentme.raw.api import get_trademe_api
    from rentme.raw.models import listings
    from api.trademe.errors import TradeMeError

    misses = 0
    hits = 0

    async def get_insight(api, listing_id):
        nonlocal hits, misses
        try:
            await api.detail.insights(listing_id)
            hits += 1
        except TradeMeError as e:
            misses += 1
            if e.description == 'No details were found for the external system id provided':
                print("No details found for", listing_id)
            elif e.description == {'ErrorDescription': 'No details were found for the external system id provided'}:
                print("No details found for", listing_id)
            else:
                raise
        print("Hit percentage: {:0.3f}%".format(hits * 100. / (hits + misses)))

    async with SizeBoundedTaskList(5, loop=loop) as ltl, \
            get_trademe_api(loop=loop) as api:
        for listing in listings.ListedItemDetail.objects.all():
            ltl.add_coro(get_insight(api, listing.listing_id))
        for idx, lstng in enumerate(ltl.as_completed()):
            await lstng


async def migrate_all_listings(enable_filtering=False):
    from django.db.models import Q
    from aioutils.task_queues import SizeBoundedTaskList
    from rentme.data.models import listings as data_listings
    from rentme.raw.models import listings as raw_listings
    from rentme.raw.importer.data_migrations.listings import migrate_listing

    print("Initilizing listing migration")
    filters = Q()
    if enable_filtering:
        all_data_listing_ids = [
            listing.listing_id
            for listing in data_listings.Listing.objects.filter(
                ~Q(suburb=None)
            )
        ]
        filters = filters | ~Q(listing_id__in=all_data_listing_ids)
    if enable_filtering:
        filters = Q(listing_id=1344948531)
    all_listings = raw_listings.ListedItemDetail.objects.filter(filters)
    num_listings = len(all_listings)
    async with SizeBoundedTaskList(20, loop=loop) as tl:
        tl.sleep_time = 1
        print("Migrating {} listings".format(num_listings))
        for listing in all_listings:
            tl.add_coro(migrate_listing(listing.listing_id))
        for idx, lstng in enumerate(tl.as_completed()):
            print("{: >6d}/{: <6d}".format(idx, num_listings))
            await lstng


async def main():
    warnings.simplefilter('error')
    asyncio.get_event_loop().set_debug(True)
    for l in [logging.getLogger('celery'),
              logging.getLogger('kombu'), logging.getLogger('rentme'),
              ]:
        l.addHandler(logging.StreamHandler())
        l.setLevel(logging.DEBUG)

    # await load_search_results()
    # await reload_catalogue()
    # await reload_listings()
    # await try_insights()
    await migrate_all_listings(False)


def model_info(model):
    from django.db.models import Count
    all_count = model.objects.count()
    for key, t in model.swagger_types.items():
        if not t.startswith('list['):
            null_count = model.objects.filter(**{key: None}).count()
        else:
            null_count = model.objects.annotate(c=Count(key)).filter(c__gt=0).count()
        yield key, null_count * 100 / all_count


if __name__ == '__main__':
    loop.run_until_complete(main())
