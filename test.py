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
import trademe.api as a
from trademe.cache import CachingClientSession, MigratingCachingStrategy, OnDiskCachingStrategy
from trademe.errors import ClassifiedExpiredError


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
    from rentme.data.importer.utils import get_trademe_api, get_trademe_session

    warnings.simplefilter('error')
    asyncio.get_event_loop().set_debug(True)
    logging.getLogger('asyncio').setLevel(logging.DEBUG)

    from rentme.raw.models import create_deserialiser
    from trademe2.api.impl import RentalSearchEndpoint
    from trademe2.api.catalouge import CategoriesEndpoint, LocalitiesEndpoint
    from trademe2.api.catalouge import MembershipLocalitiesEndpoint

    async with get_trademe_session() as session:
        deserializer = create_deserialiser()

        with session.get('v1/property/viewingtracker/' +
                         str(listing_id) + '/availableviewingtimes') as g:
            print(await g.text())


        async def call_ep(endpoint, *args, **kwargs):
            built_endpoint = endpoint(session, deserializer)
            return await built_endpoint(*args, **kwargs)

        print('CategoriesEndpoint: ', await call_ep(CategoriesEndpoint))
        print('LocalitiesEndpoint: ', await call_ep(LocalitiesEndpoint))
        print('MembershipLocalitiesEndpoint: ', await call_ep(MembershipLocalitiesEndpoint))
        value = await RentalSearchEndpoint(session, deserializer)()
        pprint(value)


if __name__ == '__main__':
    loop.run_until_complete(main())
