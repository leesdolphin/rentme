import asyncio
import decimal
import json
import urllib.parse
import warnings

from aioutils import asyncio_loop
from trademe.errors import raise_for_error_key


class TradeMeApiEndpoint:

    BASE_URI = 'https://preview.trademe.co.nz/ngapi/v1/'
    BASE_MODEL_NAME = None
    EXPECT_LIST = None
    CACHE_RESPONSE = True

    @asyncio_loop
    def __init__(self, http_requester, deserializer, *, loop):
        self.http_requester = http_requester
        self.deserializer = deserializer
        self.loop = loop

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
        return await self.loop.run_in_executor(
            None,   # Use default executor
            self.deserializer.deserialize,
            json_response, self.SWAGGER_TYPE
        )


class APIManagerBase:

    class Endpoints:
        pass

    @asyncio_loop
    def __init__(self, http_requester, deserializer, *, loop):
        super().__init__()
        self.http_requester = http_requester
        endpoints = {}
        for cls in reversed(self.__class__.mro()):
            if hasattr(cls, 'Endpoints'):
                for attr, val in cls.Endpoints.__dict__.items():
                    if len(attr) <= 1 or attr[0] == '_' or attr[-1] == '_':
                        continue
                    elif issubclass(val, APIManagerBase) or \
                            issubclass(val, TradeMeApiEndpoint):
                        endpoints[attr] = val
                    else:
                        warnings.warn(('{}.Endpoints.{} is not a supported'
                                       ' value. Check that you are listing the'
                                       ' class, and not constructing it.')
                                      .format(cls.__qualname__, attr))
        for endpoint, endpoint_cls in endpoints.items():
            endpoint_instance = endpoint_cls(http_requester=http_requester,
                                             deserializer=deserializer,
                                             loop=loop)
            setattr(self, endpoint, endpoint_instance)

    def __enter__(self):
        self.http_requester.__enter__()
        return self

    def __exit__(self, *a):
        self.http_requester.__exit__(*a)

    async def __aenter__(self):
        await self.http_requester.__aenter__()
        return self

    async def __aexit__(self, *a):
        await self.http_requester.__aexit__(*a)
