import asyncio
import trademe.models as tm_models


class TradeMeApiEndpoint():

    BASE_URI = "https://api.trademe.co.nz/"
    BASE_MODEL_NAME = None
    EXPECT_LIST = None

    def __init__(self, http_requester, model_builder):
        self.http_requester = http_requester
        self.model_builder = model_builder or tm_models.default_model_builder

    @asyncio.coroutine
    def call(self, *args, **kwargs):
        url = self.build_url(*args, **kwargs)
        response = yield from self.api_base.request('GET', url)
        return (yield from self.parse_response(response))

    def build_url(self, url_parts, base_url=None, extension='.json'):
        if base_url is None:
            base_url = self.BASE_URL
        if base_url[-1] != '/':
            base_url = base_url + '/'
        if isinstance(url_parts, str):
            url = url_parts
            if not url.endswith(extension):
                url += extension
        else:
            url = '/'.join(url_parts) + extension
        # Remove any prefixed '/'es
        while url and url[0] == '/':
            url = url[1:]
        # Remove duplicated slashes
        url = url.replace('//', '/')
        # Finally combine the base_url with the cleaned url.
        return base_url + url

    @asyncio.coroutine
    def parse_response(self, response):
        try:
            json = yield from response.json()
        except:
            json = None
        if json is None:
            raise ValueError(("Response failed to be parsed. "
                              "Status: {0.status} {0.reason}")
                             .format(response))
        if response.status >= 400 or 'ErrorDescription' in json:
            raise ValueError(("Response indicated failure. "
                              "Status: {0.status} {0.reason}. "
                              "TradeMe Reason: {1}")
                             .format(response,
                                     json.get('ErrorDescription', None)))
        return self.parse_response_json(json)

    def parse_response_json(self, json_response):
        if self.BASE_MODEL_NAME is None:
            raise ValueError(("Cannot automatically parse response if "
                              "BASE_MODEL_NAME is not defined on {}")
                             .format(self.__class__.__qualname__))
        if isinstance(json_response, list):
            if self.EXPECT_LIST is not None and not self.EXPECT_LIST:
                # Explicity said not expecting a list.
                raise ValueError(("Response was a list when it wasn't "
                                  "expected to be(using EXPECT_LIST) on {}")
                                 .format(self.__class__.__qualname__))
            output_list = []
            for item in json_response:
                output_list.append(self.model_builder(self.BASE_MODEL_NAME,
                                                      item))
            return output_list
        else:
            if self.EXPECT_LIST:
                # Explicity said expecting a list.
                raise ValueError(("Response was not a list when EXPECT_LIST "
                                  "indicates otherwise on {}")
                                 .format(self.__class__.__qualname__))
            return self.model_builder(self.BASE_MODEL_NAME, json_response)
