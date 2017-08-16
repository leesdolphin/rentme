from collections import OrderedDict
import urllib.parse


class CacheFilter():

    def filter(self, method, url, kwargs):
        return (
            self.filter_method(method),
            self.filter_url(url),
            self.filter_kwargs(kwargs),
        )

    def filter_method(self, method):
        return method.upper()

    def filter_url(self, url):
        parsed = urllib.parse.urlsplit(url)
        parsed_qs = urllib.parse.urlencode(
            sorted(urllib.parse.parse_qsl(parsed.query))
        )
        parsed = parsed._replace(query=parsed_qs)
        return urllib.parse.urlunsplit(parsed)

    def filter_kwargs(self, kwargs):
        print("Filter: ", kwargs)
        return OrderedDict(sorted(kwargs.items()))
