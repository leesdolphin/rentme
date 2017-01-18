import asyncio
import uuid

import aiohttp

import trademe.api as a

loop = asyncio.get_event_loop()

TM_CID = {'x-trademe-uniqueclientid:': 'goldilocks-' + str(uuid.uuid4())}

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Referer': 'https://preview.trademe.co.nz/property/trade-me-property/residential-to-rent/1243057304',
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
    async with aiohttp.client.ClientSession(cookies=TM_CID, headers=headers) as session:
        # y = await fetch(session, 'https://preview.trademe.co.nz/ngapi/v1/abtesting/features.json')
        api = a.RootManager(session)
        x = await api.search.rental(return_metadata=True, return_ads=True,
                                    return_super_features=True, rows=1)
        print(x)
        x = await api.listing.listing(1243057304)
        print(x)
    #     j = await fetch(session, 'https://preview.trademe.co.nz/ngapi/v1/search/property/rental.json?category=4233&return_super_features=true&rows=25&return_metadata=true&return_ads=true')
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


loop.run_until_complete(main())
