import asyncio
from datetime import datetime, timezone
import logging
import os
import traceback
import uuid
import warnings

import django

import trademe.api as a
from trademe.cache import OnDiskCachingClientSession, RateLimitingSession
from trademe.errors import ClassifiedExpiredError


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


class TestSession(RateLimitingSession, OnDiskCachingClientSession):
    pass


class NoOpSemaphore():

    def __aenter__(self):
        pass

    def __aexit__(self, *a, **k):
        pass

    async def acquire():
        return True

    def locked():
        return False

    def release():
        pass


class AsyncTaskTracker():

    def __init__(self, max_tasks=None, raise_exceptions=True):
        if max_tasks is None:
            self._task_lock = NoOpSemaphore()
        else:
            assert max_tasks > 0
            self._task_lock = asyncio.BoundedSemaphore(max_tasks)
        self._raise_exceptions = raise_exceptions
        self._task_list = []
        self._exceptions_to_raise = []

    @asyncio.coroutine
    def __aenter__(self):
        return self

    @asyncio.coroutine
    def __aexit__(self, exc_type, exc_value, traceback):
        task_list = self._task_list
        self._task_list = []
        if exc_type is not None:
            for task in task_list:
                if not task.done():
                    task.cancel()
        if task_list:
            yield from asyncio.wait(task_list)

    async def add_task(self, coro_or_future):
        if self._raise_exceptions:
            self.check_exceptions()
        success = False
        try:
            await self._task_lock.acquire()
            fut = asyncio.ensure_future(coro_or_future)
            self._task_list.append(fut)
            fut.add_done_callback(self._fut_done_callback)
            success = True
        finally:
            if not success:
                self._task_lock.release()

    def check_exceptions(self):
        if self._exceptions_to_raise:
            raise Exception() from self._exceptions_to_raise.pop()

    def _fut_done_callback(self, fut):
        self._task_lock.release()
        if fut.cancelled():
            if fut in self._task_list:
                self._task_list.remove(fut)
        else:
            try:
                fut.result()
            except Exception as e:
                self._exceptions_to_raise.append((fut, e))


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
        print('\n', listing_id)
        traceback.print_exc()
        print('Failing listing ID:', listing_id)
        try:
            input('Press enter to continue:')
        except KeyboardInterrupt:
            global exit_now
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
        await task_tracker.add_task(delete_if_missing(session, api, listing))
        await asyncio.sleep(.1)


async def main():
    import rentme.data.models.registry as registry

    warnings.simplefilter('error')
    asyncio.get_event_loop().set_debug(True)
    logging.getLogger('asyncio').setLevel(logging.DEBUG)

    from rentme.data.importer.cleanup import clean_related_tables
    from rentme.data.importer.listing import load_listing_search_results
    load_listing_search_results.delay()
    clean_related_tables()
    clean_count = 0

    try:
        async with TestSession(cache_folder=SCRIPT_DIR + '/_cache/',
                               max_inflight_requests=5, rate_limit_by_domain=True,
                               cookies=TM_CID, headers=headers) as session, \
                AsyncTaskTracker(max_tasks=20, raise_exceptions=True) as tt:
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


            return
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
