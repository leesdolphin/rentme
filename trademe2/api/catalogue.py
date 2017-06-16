from trademe2.api.base import TradeMeApiEndpoint, APIManagerBase
from trademe2.api.validation import ParameterValidator


class CategoriesEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://api.trademe.co.nz/'
    SWAGGER_TYPE = 'Category'

    @ParameterValidator.decorator(
        _booleans=('with_counts', ),
        _integers=('depth', 'region'),
        _strings=('mcat_path', ),
    )
    def build_url(self, **kwargs):
        kwargs.setdefault('rows', 25)
        return super().build_url(['v1/Categories'],
                                 params=kwargs)


class LocalitiesEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://api.trademe.co.nz/'
    SWAGGER_TYPE = 'list[Locality]'

    def build_url(self):
        return super().build_url(['v1/Localities'])


class MembershipLocalitiesEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://api.trademe.co.nz/'
    SWAGGER_TYPE = 'list[MembershipLocality]'

    def build_url(self):
        return super().build_url(['v1/TmAreas'])


class Manager(APIManagerBase):

    class Endpoints:
        membership_localities = MembershipLocalitiesEndpoint
        localities = LocalitiesEndpoint
        categories = CategoriesEndpoint
