import requests
TRADEME_API_BASE_URL = "https://api.trademe.co.nz/"
TRADEME_TOUCH_API = "https://touch.trademe.co.nz/api/"


class API(object):

    def __init__(self):
        pass

    def get_localities(self):
        return requests.get(TRADEME_API_BASE_URL + "v1/Localities.json").json()

    def get_districts(self, region):
        return requests.get(TRADEME_API_BASE_URL +
                            "v1/Localities/Region/%{region}.json"
                            .format({'region':region})
                            ).json()

    def get_suburbs(self, region, district):
        return requests.get(TRADEME_API_BASE_URL +
                            "v1/Localities/Region/%{region}/%{district}.json"
                            .format({'region':region})
                            ).json()

    def search_rental(self, params):
        return requests.get(TRADEME_TOUCH_API +
                            "v1/Search/Property/Rental.json",
                            params=params).json()

    def get_rental(self, id, params):
        return requests.get(TRADEME_TOUCH_API +
                            "v1/Listings/" + id + ".json",
                            params=params).json()


class HttpRequester(object):

    def __init__(self, base_uri, **kwargs):
        self.kwargs = kwargs
        self.base_uri = base_uri

    def get_json(self, url, format_args=None):
        if format_args is not None:
            url = url.format(format_args)
        return requests.get(self.base_uri + url, **self.kwargs).json()

# https://touch.trademe.co.nz/api/v1/Search/Property/Rental.json?132=FLAT&search=1&sidebar=1&category=4233&page=1&rows=240&return_metadata=true
