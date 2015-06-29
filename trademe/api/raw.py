import asyncio

def get_localities(http_requester):
    return http_requester.get_json("v1/Localities.json")


def get_districts(http_requester, region):
    return (yield from http_requester.get_json("v1/Localities/Region/%{region}"
                                               ".json", {'region': region}))


def get_suburbs(http_requester, region, district):
    return (yield from http_requester.get_json("v1/Localities/Region/"
                                               "%{region}/%{district}.json",
                                               {'region': region,
                                                'district': district}))



# https://api.trademe.co.nz/v1/Search/Property/Rental.
