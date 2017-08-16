from api.base.manager import APIManagerBase
from api.base.validation import build_enum_validator, build_list_validator
from api.base.validation import ParameterValidator, validate_int
from api.trademe.base import TradeMeApiEndpoint
from api.trademe.enums import PhotoSize, PropertyType, SearchSortOrder

SearchParameterValidator = ParameterValidator.decorator(
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
    _passthrough=('loop', ),
    sort_order=build_enum_validator(SearchSortOrder),
    photo_size=build_enum_validator(PhotoSize),
    property_type=build_list_validator(build_enum_validator(PropertyType),
                                       str_sep=','),
    suburb=build_list_validator(validate_int, str_sep=','),
)


class RentalSearchEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://touch.trademe.co.nz/api/'
    SWAGGER_TYPE = 'Properties'
    CACHE_RESPONSE = False

    @SearchParameterValidator
    def build_url(self, **kwargs):
        kwargs.setdefault('rows', 25)
        return super().build_url(['v1/Search/Property/Rental'],
                                 params=kwargs)


class FlatmateSearchEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://touch.trademe.co.nz/api/'
    SWAGGER_TYPE = 'Flatmates'
    CACHE_RESPONSE = False

    @SearchParameterValidator
    def build_url(self, **kwargs):
        kwargs.setdefault('rows', 25)
        return super().build_url(['v1/Search/Flatmates'],
                                 params=kwargs)


class Manager(APIManagerBase):

    class Endpoints:
        rental = RentalSearchEndpoint
        flatmate = FlatmateSearchEndpoint
