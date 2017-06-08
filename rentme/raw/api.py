import asyncio
import decimal
import json
import urllib.parse

from trademe.errors import raise_for_error_key


class TradeMeApiEndpoint:

    BASE_URI = 'https://preview.trademe.co.nz/ngapi/v1/'
    BASE_MODEL_NAME = None
    EXPECT_LIST = None
    CACHE_RESPONSE = True

    def __init__(self, http_requester, deserializer):
        self.http_requester = http_requester
        self.deserializer = deserializer

    @asyncio.coroutine
    def __call__(self, *args, **kwargs):
        url = self.build_url(*args, **kwargs)
        response = yield from self.http_requester.request(
            'GET', url, no_cache=not self.CACHE_RESPONSE)
        return (yield from self.parse_response(response))

    call = __call__

    def build_url(self, url_parts, base_url=None,
                  extension='.json', params=None):
        if base_url is None:
            base_url = self.BASE_URI
        if base_url[-1] != '/':
            base_url = base_url + '/'
        if isinstance(url_parts, str):
            url = url_parts
            if not url.endswith(extension):
                url += extension
        else:
            url = '/'.join(url_parts) + extension
        if params:
            url = url + '?' + urllib.parse.urlencode(params)
        # Remove any prefixed '/'es
        while url and url[0] == '/':
            url = url[1:]
        # Remove duplicated slashes
        url = url.replace('//', '/')
        # Finally combine the base_url with the cleaned url.
        return base_url + url

    async def parse_response(self, response):
        try:
            text = await response.text()
            data = json.loads(text, parse_float=decimal.Decimal)
        except:
            response.raise_for_status()
            raise ValueError('Response failed to be parsed.')
        raise_for_error_key(data)
        response.raise_for_status()
        try:
            return await self.parse_response_json(data)
        except Exception as e:
            raise ValueError('Cannot parse response for data: \n' +
                             self.__class__.__name__)

    async def parse_response_json(self, json_response):
        if self.SWAGGER_TYPE is None:
            raise ValueError(('Cannot automatically parse response if'
                              ' SWAGGER_TYPE is not defined on {}. Consider'
                              ' setting SWAGGER_TYPE or overiding'
                              ' `.parse_response_json(json_response)` to'
                              ' provide custom parsing.')
                             .format(self.__class__.__qualname__))
        return self.deserializer.deserialize(json_response, self.SWAGGER_TYPE)


class ListingEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://touch.trademe.co.nz/api/'
    SWAGGER_TYPE = 'ListedItemDetail'

    def build_url(self, listing_id):
        return super().build_url(['v1/Listings', str(listing_id)],
                                 params=dict(
                                     return_member_profile=True,
                                     increment_view_count=False,
        ))
