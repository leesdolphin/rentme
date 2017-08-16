import uuid
import urllib.parse

from aioutils.aiohttp.cache.filter import CacheFilter
from api.trademe.errors import raise_for_error_key
from api.base.endpoint import BaseSwaggerEndpoint


class TradeMeCacheFilter(CacheFilter):

    def filter_kwargs(self, kwargs):
        return {}


class TradeMeApiEndpoint(BaseSwaggerEndpoint):

    BASE_URI = 'https://preview.trademe.co.nz/ngapi/v1/'

    def build_request(self, *args, **kwargs):
        tm_uid = 'goldilocks-' + str(uuid.uuid4())
        method = 'GET'
        url = self.build_url(*args, **kwargs)
        opts = dict(
            headers={
                'Referer': ('https://preview.trademe.co.nz/property/'
                            'trade-me-property/residential-to-rent/123456789'),
                'Cache-Control': 'no-cache',
                'x-trademe-uniqueclientid': tm_uid,
                'Cookie': 'x-trademe-uniqueclientid=' + tm_uid,
            },
            cache_filter=TradeMeCacheFilter(),
        )
        return method, url, opts

    def raise_for_data_error(self, data):
        raise_for_error_key(data)

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
