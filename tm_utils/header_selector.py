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
                if res:
                    print('Found valid combination with cookie names:',
                          ', '.join([ck.partition('=')[0] for ck in res]))
                    all_results.append(res)
                else:
                    cookies.remove(check_cookie)
    return all_results


async def try_cookie_combinations(url, headers, cookies):
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
            if any(results):
                all_results += filter(None, results)
                valid_cookies = set(cookies)
                for res in filter(None, results):
                    print('Found valid combination with cookie names:',
                          ', '.join([ck.partition('=')[0] for ck in res]))
                    valid_cookies &= set(res)
                if valid_cookies:
                    cookies &= valid_cookies
                else:
                    # All combinations were valid, we're not going to get
                    # anywhere from here.
                    break
            if perms > len(cookies):
                perms = len(cookies)
            else:
                perms = perms - 1
    return all_results


async def main():
    url, headers = parse_headers_from_stdin()
    cookies = parse_cookies(headers.get('cookie', ''))
    res = await asyncio.gather(
        try_cookie_combinations(url, headers, cookies),
        try_cookie_removal(url, headers, cookies),
    )
    all_results = list(itertools.chain(*res))
    min_len = min(len(res) for res in all_results)
    valid_cookie_combos = filter(lambda res: len(res) == min_len, all_results)
    for combo in valid_cookie_combos:
        print('Found valid combination with cookie names:',
              ', '.join([ck.partition('=')[0] for ck in combo]))


if __name__ == '__main__':
    loop.run_until_complete(main())
