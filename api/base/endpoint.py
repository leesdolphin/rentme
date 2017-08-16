from abc import ABCMeta, abstractmethod
import asyncio
import aiohttp
import decimal
import json

from aioutils import asyncio_loop

from api.error import ApiConnectionError, ApiError


class BaseEndpoint(metaclass=ABCMeta):

    BASE_URI = 'https://preview.trademe.co.nz/ngapi/v1/'
    CACHE_RESPONSE = True

    @asyncio_loop
    def __init__(self, *, loop, http_requester):
        self.http_requester = http_requester
        self.loop = loop

    @asyncio.coroutine
    def __call__(self, *args, **kwargs):
        method, url, kwargs = self.build_request(*args, **kwargs)
        if not kwargs:
            kwargs = {}
        kwargs.setdefault('no_cache', not self.CACHE_RESPONSE)
        retries = 3
        while retries >= 0:
            try:
                response = yield from self.http_requester.request(
                    method, url, **kwargs)
                break
            except aiohttp.ClientConnectorError as e:
                if retries:
                    retries -= 1
                else:
                    raise ApiConnectionError(url=url) from e
        try:
            return (yield from self.parse_response(response))
        except ApiError as e:
            raise e
        except aiohttp.ClientError as e:
            raise ApiError(url=url) from e
        except Exception as e:
            raise ApiError(url=url) from e

    call = __call__

    @abstractmethod
    def build_request(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def parse_response(self, response):
        pass


class BaseJsonEndpoint(BaseEndpoint, metaclass=ABCMeta):

    async def parse_response(self, response):
        try:
            text = await response.text()
            data = json.loads(text, parse_float=decimal.Decimal)
        except:
            response.raise_for_status()
            raise ValueError('Response failed to be parsed.')
        self.raise_for_data_error(data)
        self.raise_for_response_error(response)
        try:
            return await self.parse_response_json(data)
        except Exception as e:
            raise ValueError('Cannot parse response for data: \n' +
                             self.__class__.__name__)

    def raise_for_response_error(self, response):
        response.raise_for_status()

    def raise_for_data_error(self, data):
        pass

    @abstractmethod
    async def parse_response_json(self, json_response):
        pass


class BaseSwaggerEndpoint(BaseJsonEndpoint, metaclass=ABCMeta):

    @asyncio_loop
    def __init__(self, deserializer, **kwargs):
        super().__init__(**kwargs)
        self.deserializer = deserializer
        if not hasattr(self, 'SWAGGER_TYPE'):
            raise AttributeError(
                'Missing SWAGGER_TYPE on {}.'.format(type(self).__qualname__)
            )

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
