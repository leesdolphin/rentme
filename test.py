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
    logging.getLogger('asyncio').setLevel(logging.DEBUG)

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
    fm = dict(model_info(search.Flatmate))
    pr = dict(model_info(search.Property))
    lid = dict(model_info(listings.ListedItemDetail))

    x = {
        key: max(fm.get(key, 0), pr.get(key, 0), lid.get(key, 0))
        for key in set(fm) | set(pr) | set(lid)
    }
    has = {k: v for k, v in x.items() if v < 100}

    print('\n'.join(sorted(k for k, v in has.items() if v == 0)))
    print()
    print('\n'.join("%s %0.3f" % (k, has[k]) for k in sorted([k for k, v in has.items() if v > 0], key=lambda k:has[k])))
    print()
    print('\n'.join("%s 100" % (k) for k in sorted(set(x) - set(has))))


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
