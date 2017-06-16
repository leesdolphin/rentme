from trademe2.api.base import APIManagerBase, TradeMeApiEndpoint


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
                                  '/availableviewingtimes.json'],)


class Manager(APIManagerBase):

    class Endpoints:
        listing = ListingEndpoint
        viewing_times = ViewingTimesEndpoint
