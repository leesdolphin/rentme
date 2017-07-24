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
# import trademe.api as a
# from trademe.cache import CachingClientSession, MigratingCachingStrategy, OnDiskCachingStrategy
# from trademe.errors import ClassifiedExpiredError


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentme.settings')
    django.setup()

loop = asyncio.get_event_loop()

SCRIPT_DIR = os.path.dirname(__file__)


async def main():
    # import rentme.data.models.registry as registry
    # from rentme.data.importer.cleanup import clean_related_tables
    # from rentme.data.importer.models import CachedResponse
    # from rentme.data.importer.listing import load_listing_search_results, delete_all_outdated, load_listing
    # from rentme.data.models.listing import Listing, Agency
    # from rentme.data.importer.postprocessing import postprocess_listing, process_listing_price
    # from rentme.data.importer.utils import DatabaseCachingStrategy
    # from rentme.data.importer.utils import get_trademe_api, get_trademe_session

    warnings.simplefilter('error')
    asyncio.get_event_loop().set_debug(True)
    for l in [logging.getLogger('celery'),
              logging.getLogger('kombu'), logging.getLogger('rentme'),
              ]:
        l.addHandler(logging.StreamHandler())
        l.setLevel(logging.DEBUG)
    # import rentme.raw.importer.catalogue as catalogue

    # import rentme.raw.importer.listing as listing
    # import cProfile
    # pr = cProfile.Profile()
    # pr.enable()
    # try:
    #     await asyncio.gather(
    #         listing.load_flatmate_listing_search_results(),
    #         listing.load_rental_listing_search_results(),
    #     )
    # finally:
    #     pr.create_stats()
    #     pr.dump_stats('/code/test.profile')
    #     # pr.print_stats()

    from rentme.raw.models import listings, search
    from rentme.raw.importer.listing import load_listings
    from rentme.raw.importer.listing import load_rental_listing_search_results
    from rentme.raw.importer.listing import load_flatmate_listing_search_results
    from rentme.raw.importer.data_migrations.listings import migrate_listing
    from rentme.raw.importer.data_migrations.members import migrate_member
    from rentme.raw.importer.data_migrations.error import ModelDataMissing


    from aioutils.celery import asyncio_task, delay_or_call
    from aioutils.task_queues import SizeBoundedTaskList
    from celery.utils.log import get_task_logger
    from trademe.errors import ClassifiedExpiredError

    from rentme.raw.api import get_trademe_api


    # await load_rental_listing_search_results()
    # await load_flatmate_listing_search_results()
    async with SizeBoundedTaskList(2, loop=loop) as ltl, \
            get_trademe_api(loop=loop) as api:
        for listing in search.Flatmate.objects.all():
            ltl.add_coro(api.detail.listing(listing.listing_id))
        for listing in search.Property.objects.all():
            ltl.add_coro(api.detail.listing(listing.listing_id))
        for listing in listings.ListedItemDetail.objects.all():
            ltl.add_coro(api.detail.listing(listing.listing_id))
        for i in ltl.as_completed():
            try:
                await i
            except:
                pass
    i = 0
    for listing in listings.ListedItemDetail.objects.all():
        try:
            await migrate_listing(listing.listing_id)
        except ModelDataMissing:
            print("Model data missing for listing", listing.listing_id)
            print('\t\t\t\t\tProcessed Items: ', i)
            load_listings.delay([listing.listing_id])
            i = 0
            continue
        else:
            i += 1


    for listing in listings.ListedItemDetail.objects.all():
        try:
            await migrate_member(listing.member.member_id)
            await migrate_listing(listing.listing_id)
        except ModelDataMissing:
            print("Model data missing for listing", listing.listing_id)
            print('\t\t\t\t\tProcessed Items: ', i)
            load_listings.delay([listing.listing_id])
            i = 0
            continue
        else:
            i += 1
    fm = dict(model_info(search.Flatmate))
    pr = dict(model_info(search.Property))
    lid = dict(model_info(listings.ListedItemDetail))

    x = {
        key: max(fm.get(key, 0), pr.get(key, 0), lid.get(key, 0))
        for key in set(fm) | set(pr) | set(lid)
    }
    has = {k: v for k, v in x.items() if v < 100}


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
