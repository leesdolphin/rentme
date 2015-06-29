from trademe.api.tag import no_auth
import asyncio
import aiohttp
__author__ = 'lee'

@asyncio.coroutine
def _req_json(session, *args, **kw):
    resp = yield from session.request(*args, **kw)
    if resp.status == 200:
        return (yield from resp.json())
    else:
        raise Exception("Fu Bar")



@no_auth
@asyncio.coroutine
def get_localities(session):
    return (yield from _req_json(session,
                                 'get', session.root + "v1/Localities.json"))


@no_auth
@asyncio.coroutine
def get_districts(session, region):
    url = session.root + "v1/Localities/Region/%{region}.json"
    return (yield from _req_json(session,
                                 'get', url.format({'region': region})))


@no_auth
@asyncio.coroutine
def get_suburbs(session, region, district):
    url = session.root + "v1/Localities/Region/%{region}/%{district}.json"
    return (yield from _req_json(session,
                                 'get', url.format({'region': region,
                                                    'district': district})))

