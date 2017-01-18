#!/usr/bin/python
'''
Runs through the cookies used in an existing request and attemts to reduce the
number required to send.

'''

import asyncio
import itertools

import aiohttp

from tm_utils.utils import NullCookieJar, parse_cookies, parse_headers_from_stdin


loop = asyncio.get_event_loop()


async def try_cookies(session, url, cookies):
    session.cookie_jar.clear()
    cookie_str = '; '.join(cookies) + '; '
    try:
        async with session.get(url, headers={
                    'Cookie': cookie_str
                }) as response:
            print(response.request.cookies)
            status = response.status
    except:
        return None
    if status == 200:
        return cookies
    else:
        return None


async def try_cookie_removal(url, headers, cookies):
    cookies = set(cookies)
    all_results = []
    async with aiohttp.client.ClientSession(cookie_jar=NullCookieJar(),
                                            headers=headers) as session:
        prev = 0
        while prev != len(cookies):
            prev = len(cookies)
            for check_cookie in set(cookies):
                cks = set(cookies) - set([check_cookie])
                res = await try_cookies(session, url, cks)
                if res is None or res is False:
                    cookies.remove(check_cookie)
                else:
                    print('Found valid combination with cookie names:',
                          ', '.join([ck.partition('=')[0] for ck in res]))
                    all_results.append(res)
    return all_results


async def try_cookie_combinations(url, headers, cookies):
    orig_len = len(cookies)
    cookies = set(cookies)
    all_results = []
    attempt_removal = False
    async with aiohttp.client.ClientSession(cookie_jar=NullCookieJar(),
                                            headers=headers) as session:
        perms = len(cookies)
        while perms > 0:
            wait_arr = []
            if not all_results:
                wait_arr.append(try_cookies(session, url, []))
            for cks in itertools.combinations(cookies, perms):
                wait_arr.append(try_cookies(session, url, cks))
            print('Cookie count: ', (perms), 'Execution count: ', len(wait_arr))
            future_arr = asyncio.gather(*wait_arr)
            try:
                results = await future_arr
            except:
                future_arr.cancel()
                raise
            valid_res = list(filter(lambda r: r is not None and r is not False, results))
            print(results, valid_res)
            if valid_res:
                all_results += valid_res
                for res in valid_res:
                    cookies &= set(res)
            elif len(cookies) == orig_len:
                # Cannot find any for the original length. No hope for deeper.
                return []
            if perms > len(cookies):
                perms = len(cookies)
            else:
                perms = perms - 1
    return all_results


async def main():
    url, headers = parse_headers_from_stdin()
    cookies = parse_cookies(headers.get('cookie', ''))
    futs = [
        try_cookie_combinations(url, headers, cookies),
        try_cookie_removal(url, headers, cookies),
    ]
    all_results = []
    for result_co in asyncio.as_completed(futs):
        results = await result_co
        all_results += results
        if not results:
            break
        min_len = min(len(res) for res in results)
        if min_len < 2:
            break
    asyncio.gather(futs).cancel()

    if not all_results:
        print("No combinations found")
        return
    min_len = min(len(res) for res in all_results)
    valid_cookie_combos = filter(lambda res: len(res) == min_len, all_results)
    for combo in valid_cookie_combos:
        print('Found valid combination with cookie names:',
              ', '.join([ck.partition('=')[0] for ck in combo]))


if __name__ == '__main__':
    loop.run_until_complete(main())
