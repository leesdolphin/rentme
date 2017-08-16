from api.trademe.base import TradeMeApiEndpoint
from api.base.manager import APIManagerBase


class ListingEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://preview.trademe.co.nz/ngapi/'
    SWAGGER_TYPE = 'ListedItemDetail'

    def build_url(self, listing_id):
        return super().build_url(['v1/Listings', str(listing_id)],
                                 params=dict(
                                     return_member_profile=True,
                                     increment_view_count=False,
        ))


class ViewingTimesEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://preview.trademe.co.nz/ngapi/'
    SWAGGER_TYPE = 'ViewingTimes'

    def build_url(self, listing_id):
        return super().build_url(['v1/property/viewingtracker/',
                                  str(listing_id),
                                  '/availableviewingtimes'],)


class PropertyInsightsEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://preview.trademe.co.nz/ngapi/'
    SWAGGER_TYPE = None

    def build_url(self, listing_id):
        return super().build_url(['property/insights/details/TradeMeListings/',
                                  str(listing_id)],)

    async def parse_response_json(self, response_json):
        import os
        import json
        pid = response_json['Id']
        os.makedirs('/code/insights/raw', exist_ok=True)
        os.makedirs('/code/insights/struct', exist_ok=True)
        with open('/code/insights/struct/' + str(pid) + '.txt', 'w') as f:
            f.write('\n'.join(sorted(build_data_structure(response_json))))
            f.write('\n')
        with open('/code/insights/raw/' + str(pid) + '.json', 'w') as f:
            json.dump(response_json, f, default=str, indent=2)


def build_data_structure(obj, path=''):
    items = set()
    if isinstance(obj, dict):
        for key, v in obj.items():
            items.update(build_data_structure(v, path + '.' + key))
    elif isinstance(obj, list):
        for item in obj:
            items.update(build_data_structure(item, path + '[]?'))
    else:
        items.add('{:<70s}: {}'.format(path, type(obj).__qualname__))
    return items


class Manager(APIManagerBase):

    class Endpoints:
        insights = PropertyInsightsEndpoint
        listing = ListingEndpoint
        viewing_times = ViewingTimesEndpoint
