import datetime

from trademe.api.base import APIManagerBase, TradeMeApiEndpoint
from trademe.api.registry import parser_registry
from trademe.models.enums import PhotoSize, PropertyType, SearchSortOrder
from trademe.utils import reduce_mapping, title_to_snake_case_mapping


class RentalSearchEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://touch.trademe.co.nz/api/'
    BASE_MODEL_NAME = 'search.SearchResults'
    EXPECT_LIST = False

    def build_url(self, rows=25, **kwargs):
        tm_params = {'rows': rows}
        booleans = ['adjacent_suburbs', 'available_now', 'pets_ok',
                    'return_metadata', 'return_ads', 'return_super_features']
        integers = ['bathrooms_max', 'bathrooms_min', 'bedrooms_max',
                    'bedrooms_min', 'district', 'member_listing', 'page',
                    'price_max', 'price_min', 'region']
        datetimes = ['date_from']
        strings = ['search_string']

        if 'sort_order' in kwargs:
            tm_params['sort_order'] = SearchSortOrder(kwargs.pop('sort_order')).name
        if ('latitude_max' in kwargs or
                'latitude_min' in kwargs or
                'longitude_max' in kwargs or
                'longitude_min' in kwargs):
            if not ('latitude_max' in kwargs and
                    'latitude_min' in kwargs and
                    'longitude_max' in kwargs and
                    'longitude_min' in kwargs):
                raise ValueError('Missing one or more of the lat/long ranges.')
            tm_params['latitude_max'] = kwargs.pop('latitude_max')
            tm_params['latitude_min'] = kwargs.pop('latitude_min')
            tm_params['longitude_max'] = kwargs.pop('longitude_max')
            tm_params['longitude_min'] = kwargs.pop('longitude_min')
        if 'photo_size' in kwargs:
            if kwargs['photo_size'] not in PhotoSize.__members__:
                raise ValueError('The value given for `photo_size` is not a '
                                 'member of the `PhotoSize` Enum. Given %r'
                                 % (kwargs['photo_size']))
            tm_params['photo_size'] = kwargs.pop('photo_size')
        if 'property_type' in kwargs:
            old_pt = kwargs.pop('property_type')
            if isinstance(old_pt, str):
                if ',' in old_pt:
                    old_pt = old_pt.split(',')
                elif old_pt:
                    old_pt = [old_pt]
                else:
                    old_pt = []
            for item in old_pt:
                if item not in PropertyType.__members__:
                    raise ValueError('An item of `property_type` is not a '
                                     'member of the `PropertyType` Enum. Given '
                                     '%r, erroring value %r'
                                     % (kwargs['property_type'], item))
            tm_params['property_type'] = ','.join(old_pt)
            del old_pt
        if 'suburb' in kwargs:
            old_suburb = kwargs.pop('suburb')
            if isinstance(old_suburb, str):
                if ',' in old_suburb:
                    old_suburb = old_suburb.split(',')
                elif old_suburb:
                    old_suburb = [old_suburb]
                else:
                    old_suburb = []
            for item in old_suburb:
                try:
                    int(item)
                except ValueError as ve:
                    raise ValueError('An item of `suburb` is not an integer. '
                                     'Given %r, erroring value %r'
                                     % (kwargs['suburb'], item)) from ve
            tm_params['suburb'] = ','.join(old_suburb)
        for key in strings:
            if key in kwargs:
                tm_params[key] = kwargs.pop(key)
        for key in datetimes:
            if key in kwargs:
                dt = kwargs.pop(key)
                assert isinstance(dt, datetime.datetime), \
                    ('Key %r is not a datetime object. Got %r' % (key, dt))
                ts_millis = dt.timestamp() * 1000
                # '%d' truncates any decimal places.
                tm_params[key] = '/Date(%d)/' % (ts_millis, )
        for key in integers:
            if key in kwargs:
                value = kwargs.pop(key)
                try:
                    int(value)
                except ValueError as ve:
                    raise ValueError('Key %r is not an integer. Got %r' % (key, dt)) from ve
                tm_params[key] = value
        for key in booleans:
            if key in kwargs:
                tm_params[key] = 'true' if kwargs.pop(key) else 'false'
        if kwargs:
            raise ValueError('Some unknown arguments were passed in: %r' % (kwargs.keys()))
        return super().build_url(['v1/Search/Property/Rental'],
                                 params=tm_params)


@parser_registry.register('search.SearchResults', auto_model=True)
def parse_listing(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        name_mapping=title_to_snake_case_mapping(
            'Parameters', 'List', 'PageSize',
            'TotalCount', 'SuperFeatures', 'Page'),
        ignore_keys=['FoundCategories', 'Ads', 'Parameters', 'SortOrders'])
    data['list'] = data.pop('super_features', []) + data.pop('list', [])
    listing_ids = []
    for list_item in data['list']:
        listing_ids.append(list_item['ListingId'])
    data['list'] = listing_ids
    return data


class Manager(APIManagerBase):

    class Endpoints:
        rental = RentalSearchEndpoint
