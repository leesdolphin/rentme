import asyncio
import collections
import hashlib
import os
import pathlib
import pickle
import traceback
import urllib.parse
import uuid

import aiohttp
import multidict
import django

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rentme.settings")
    django.setup()

import trademe.api as a
from trademe.cache import OnDiskCachingClientSession, CachedResponse
import rentme.web.models.registry as registry
import rentme.web.models.catalogue as catalogue

loop = asyncio.get_event_loop()

SCRIPT_DIR = os.path.dirname(__file__)

TM_CID = {'x-trademe-uniqueclientid:': 'goldilocks-' + str(uuid.uuid4())}

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Referer': 'https://preview.trademe.co.nz/property/trade-me-property'
               '/residential-to-rent/1243057304',
    'Cache-Control': 'no-cache',
    # 'Cache-Control': 'no-cache',
    # 'Cache-Control': 'max-stale',
    # 'Cache-Control': 'no-store',
    # 'Cache-Control': 'min-fresh=1000',
    # 'Cache-Control': 'no-transform',
    # 'Cache-Control': 'only-if-cached',
    # 'Cache-Control': 'must-revalidate',


}
headers.update(TM_CID)


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


async def main():
    async with OnDiskCachingClientSession(cache_folder=SCRIPT_DIR + '/_cache/',
                                          cookies=TM_CID, headers=headers) as session:
        api = a.RootManager(session, model_registry=registry.model_registry)
        print(sorted(map(lambda s: s.suburb_id, catalogue.Suburb.objects.all())))

        search_res = await api.search.rental(return_metadata=True, return_ads=True,
                                             return_super_features=True, rows=25, page=1)
        seen_errors = set()
        for page_no in range(1, int(search_res.total_count / search_res.page_size)):
            search_cache_info = session.cache_info
            search_res = await api.search.rental(return_metadata=True, return_ads=True,
                                                 return_super_features=True, rows=25, page=page_no)
            print("\nPage", page_no)
            for listing_id in sorted(search_res.list):
                cache_misses = session.cache_info.misses
                try:
                    x = await api.listing.listing(listing_id)
                    print('.', end='', flush=True)
                except Exception as e:
                    print('\n', listing_id)
                    if e not in seen_errors:
                        seen_errors.add(e)
                        traceback.print_exc()
                        input('Press enter to continue:')
                if cache_misses != session.cache_info.misses:
                    # return
                    await asyncio.sleep(1)
            if search_cache_info.misses != session.cache_info.misses:
                print("\nBefore:", search_cache_info, "After:", session.cache_info, end='', flush=True)
                # await asyncio.sleep(10)
                return
    #     j = await fetch(session, 'https://preview.trademe.co.nz/ngapi/v1/search'
    #                              '/property/rental.json?category=4233&'
    #                              'return_super_features=true&rows=25&'
    #                              'return_metadata=true&return_ads=true')
    #     wait_arr = []
    #     for item in j['List'] + j['SuperFeatures']:
    #         wait_arr.append(fetch_listing(session, item))
    #     results = await asyncio.gather(*wait_arr)
    #     j = await fetch(session,'https://touch.trademe.co.nz/api/v1/Member/5369626/Profile.json')
    #     write_out('profile_keys.txt', build_key_list(j))
    #
    # asks, alks, asknil, alknis = set(), set(), set(), set()
    # for sks, lks, sknil, lknis in results:
    #     asks |= sks
    #     alks |= lks
    #     asknil |= sknil
    #     alknis |= lknis
    # write_out('search_keys.txt', asks)
    # write_out('listing_keys.txt', alks)
    # write_out('search_unique.txt', asknil)
    # write_out('listing_unique.txt', alknis)

if __name__ == '__main__':
    loop.run_until_complete(main())
