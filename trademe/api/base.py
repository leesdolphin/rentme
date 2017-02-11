import asyncio
import decimal
import json
import urllib.parse
import warnings


class TradeMeApiEndpoint:

    BASE_URI = 'https://preview.trademe.co.nz/ngapi/v1/'
    BASE_MODEL_NAME = None
    EXPECT_LIST = None

    def __init__(self, http_requester,
                 parser_registry=None, model_registry=None):
        self.http_requester = http_requester
        if not parser_registry:
            from trademe.api.registry import parser_registry
        self.parser_registry = parser_registry
        if not model_registry:
            from trademe.models.registry import model_registry
        self.model_registry = model_registry

    @asyncio.coroutine
    def __call__(self, *args, **kwargs):
        url = self.build_url(*args, **kwargs)
        response = yield from self.http_requester.request('GET', url)
        return (yield from self.parse_response(response))

    call = __call__

    def build_url(self, url_parts, base_url=None, extension='.json', params=None):
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
            data = None
            if data is None:
                raise ValueError(('Response failed to be parsed.'
                                  ' Status: {0.status} {0.reason}')
                                 .format(response))
        if response.status >= 400 or 'ErrorDescription' in data:
            raise ValueError(('Response indicated failure.'
                              ' Status: {0.status} {0.reason}.'
                              ' TradeMe Reason: {1}')
                             .format(response,
                                     data.get('ErrorDescription', None)))
        try:
            return await self.parse_response_json(data)
        except Exception as e:
            raise ValueError('Cannot parse response for data: \n' +
                             self.__class__.__name__)

    @property
    def parser(self):
        if self.BASE_MODEL_NAME is None:
            raise ValueError(('Model name is not given on {} so cannot'
                              ' automatically get parser. Use'
                              ' `.get_parser(<desired parser>)` instead.')
                             .format(self.__class__.__qualname__))
        return self.get_parser(self.BASE_MODEL_NAME)

    def get_parser(self, name):
        return self.parser_registry.get_parser(
            name,
            model_registry=self.model_registry,
            parser_registry=self.parser_registry)

    async def parse_response_json(self, json_response):
        if self.BASE_MODEL_NAME is None:
            raise ValueError(('Cannot automatically parse response if'
                              ' BASE_MODEL_NAME is not defined on {}. Consider'
                              ' setting BASE_MODEL_NAME or overiding'
                              ' `.parse_response_json(json_response)` to'
                              ' provide custom parsing.')
                             .format(self.__class__.__qualname__))
        if isinstance(json_response, list):
            if self.EXPECT_LIST is not None and not self.EXPECT_LIST:
                # Explicity said not expecting a list.
                raise ValueError(('Response was a list when it wasn\'t'
                                  ' expected to be(using EXPECT_LIST) on {}')
                                 .format(self.__class__.__qualname__))
            output_list = []
            for item in json_response:
                output_list.append(self.parser(item))
            return await asyncio.gather(*output_list)
        else:
            if self.EXPECT_LIST:
                # Explicity said expecting a list.
                raise ValueError(('Response was not a list when EXPECT_LIST'
                                  ' indicates otherwise on {}')
                                 .format(self.__class__.__qualname__))
            return await self.parser(json_response)


class APIManagerBase:

    class Endpoints:
        pass

    def __init__(self, http_requester,
                 parser_registry=None, model_registry=None):
        super().__init__()
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
            endpoint_instance = endpoint_cls(http_requester,
                                             parser_registry, model_registry)
            setattr(self, endpoint, endpoint_instance)
