import requests
TRADEME_API_BASE_URL =
TRADEME_TOUCH_API = "https://touch.trademe.co.nz/api/"


class API(object):

    def __init__(self):
        pass



class HttpRequester(object):

    def __init__(self, base_uri, **kwargs):
        self.kwargs = kwargs

    def get_json(self, url, format_args=None):
        if format_args is not None:
            url = url.format(format_args)
        return requests.get(url, **self.kwargs).json()

# https://touch.trademe.co.nz/api/v1/Search/Property/Rental.json?132=FLAT&search=1&sidebar=1&category=4233&page=1&rows=240&return_metadata=true
