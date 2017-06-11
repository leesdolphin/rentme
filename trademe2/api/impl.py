from trademe.models.enums import PhotoSize, PropertyType, SearchSortOrder
from trademe2.api.base import TradeMeApiEndpoint
from trademe2.api.validation import build_enum_validator, build_list_validator
from trademe2.api.validation import ParameterValidator, validate_int


class ListingEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://touch.trademe.co.nz/api/'
    SWAGGER_TYPE = 'ListedItemDetail'

    def build_url(self, listing_id):
        return super().build_url(['v1/Listings', str(listing_id)],
                                 params=dict(
                                     return_member_profile=True,
                                     increment_view_count=False,
        ))


class RentalSearchEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://touch.trademe.co.nz/api/'
    SWAGGER_TYPE = 'Properties'
    CACHE_RESPONSE = False

    @ParameterValidator.decorator(
        _booleans=('adjacent_suburbs', 'available_now', 'pets_ok',
                   'return_metadata', 'return_ads', 'return_super_features'),
        _integers=('bathrooms_max', 'bathrooms_min', 'bedrooms_max',
                   'bedrooms_min', 'district', 'member_listing', 'page',
                   'price_max', 'price_min', 'region', 'rows'),
        _floats=('latitude_max', 'latitude_min',
                 'longitude_max', 'longitude_min'),
        _datetimes=('date_from', ),
        _strings=('search_string', ),
        _exists_together=(
            ('latitude_max', 'latitude_min', 'longitude_max', 'longitude_min'),
        ),
        sort_order=build_enum_validator(SearchSortOrder),
        photo_size=build_enum_validator(PhotoSize),
        property_type=build_list_validator(build_enum_validator(PropertyType),
                                           str_sep=','),
        suburb=build_list_validator(validate_int, str_sep=','),
    )
    def build_url(self, **kwargs):
        kwargs.setdefault('rows', 25)
        return super().build_url(['v1/Search/Property/Rental'],
                                 params=kwargs)
