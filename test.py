import asyncio
from datetime import datetime, timezone
import logging
import os
import traceback
import uuid
import warnings

import django

import trademe.api as a
from trademe.cache import CachingClientSession, OnDiskCachingStrategy, RateLimitingSession, MigratingCachingStrategy
from trademe.errors import ClassifiedExpiredError
from aioutils.task_queues import AsyncTaskTracker

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentme.settings')
    django.setup()

loop = asyncio.get_event_loop()

SCRIPT_DIR = os.path.dirname(__file__)

TM_CID = {'x-trademe-uniqueclientid:': 'goldilocks-' + str(uuid.uuid4())}

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Referer': 'https://preview.trademe.co.nz/property/trade-me-property'
               '/residential-to-rent/1243057304',
    'Cache-Control': 'no-cache',
}
headers.update(TM_CID)


class TestSession(RateLimitingSession, CachingClientSession):
    pass


async def fetch(session, *args, **kwargs):
    print(args, kwargs)
    async with session.get(*args, **kwargs) as response:
        print(response)
        print(response.headers)
        json = await response.json()
        return json


def write_out(filename, key_set):
    with open(filename, 'w') as f:
        f.write('\n'.join(sorted(key_set)))


exit_now = False


async def load_listing(api, listing_id):
    global exit_now
    from rentme.data.models.listing import Listing
    try:
        try:
            Listing.objects.get(listing_id=listing_id).delete()
        except Listing.DoesNotExist:
            pass
        misses = api.listing.listing.http_requester.cache_info.misses
        listing = await api.listing.listing(listing_id)
        print(listing_id, ': ', listing)
        if api.listing.listing.http_requester.cache_info.misses > misses:
            await asyncio.sleep(10)
    except ClassifiedExpiredError as e:
        print('Classified expired:', listing_id)
        return
    except Exception as e:
        if exit_now:
            return
        print('\n', listing_id)
        traceback.print_exc()
        print('Failing listing ID:', listing_id)
        try:
            input('Press enter to continue:')
        except KeyboardInterrupt:
            exit_now = True
            return


async def check_listing_exists(session, listing_id):
    url = ('http://www.trademe.co.nz/property/residential-property-to-rent/'
           'auction-%s.htm' % (listing_id, ))
    async with session.head(url, no_cache=True) as response:
        if response.status == 200:
            return True
        else:
            return False


async def delete_if_missing(session, api, listing):
    if not await check_listing_exists(session, listing.listing_id):
        print('Deleting listing', listing.listing_id)
        listing.delete()
    else:
        await load_listing(api, listing.listing_id)


async def delete_all_outdated(task_tracker, session, api):
    from rentme.data.models.listing import Listing
    for listing in Listing.objects.filter(end_date__lt=datetime.now(tz=timezone.utc)):
        await task_tracker.add_task()
        await asyncio.sleep(.1)


async def main():
    import rentme.data.models.registry as registry
    from rentme.data.importer.cleanup import clean_related_tables
    from rentme.data.importer.listing import load_listing_search_results, delete_all_outdated
    from rentme.data.importer.utils import DatabaseCachingStrategy

    warnings.simplefilter('error')
    asyncio.get_event_loop().set_debug(True)
    logging.getLogger('asyncio').setLevel(logging.DEBUG)

    load_listing_search_results.delay()
    delete_all_outdated.delay()
    clean_related_tables.delay()
    return
    clean_count = 0

    cache_strategy = MigratingCachingStrategy(
        primary_cache=DatabaseCachingStrategy(),
        old_caches=(
            OnDiskCachingStrategy(cache_folder=SCRIPT_DIR + '/_cache/'),
        ))
    try:
        async with TestSession(cache_strategy=cache_strategy,
                               max_inflight_requests=5,
                               rate_limit_by_domain=True,
                               cookies=TM_CID, headers=headers) as session, \
                AsyncTaskTracker(max_tasks=20000, raise_exceptions=True) as tt:
            api = a.RootManager(session, model_registry=registry.model_registry)
            # for lid in ['1306451550']:
            #     await load_listing(api, lid)
            # return

            search_kwargs = dict(return_metadata=True, return_ads=True,
                                 return_super_features=True, sort_order='ExpiryDesc',
                                 rows=25)
            search_res = await api.search.rental(**search_kwargs, page=1)
            print(search_res.total_count)
            pages = int(search_res.total_count / search_res.page_size) + 1
            # await tt.add_task(delete_all_outdated(tt, session, api))


            # return
            for page_no in range(1, pages + 1):
                misses = session.cache_info.misses
                print('\nPage', page_no, '/', pages)
                search_res = await api.search.rental(return_metadata=True, return_ads=True,
                                                     sort_order='ExpiryDesc',
                                                     return_super_features=True, rows=25, page=page_no)
                for listing_id in sorted(search_res.list):
                    if exit_now:
                        return
                    # if not listing_models.Listing.objects.filter(
                    #         listing_id=int(listing_id)).exists():
                    await tt.add_task(load_listing(api, listing_id))
                if session.cache_info.misses > misses:
                    clean_count = 0
                    # print('Sleeping')
                    # await asyncio.sleep(1)
                    # await tt.add_task(asyncio.sleep(10))
                elif clean_count < 100:
                    clean_count += 1
                else:
                    break
                if exit_now:
                    return
    finally:
        clean_related_tables()


if __name__ == '__main__':
    loop.run_until_complete(main())
