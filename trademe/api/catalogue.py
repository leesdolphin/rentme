from trademe.api.base import APIManagerBase, TradeMeApiEndpoint
from trademe.api.registry import parser_registry
from trademe.models import enums
from trademe.utils import date_convert, enum_convert, parser_convert_lists
from trademe.utils import reduce_mapping, title_to_snake_case_mapping


class CategoriesEndpoint(TradeMeApiEndpoint):

    BASE_MODEL_NAME = 'catalogue.Category'
    EXPECT_LIST = False

    def build_url(self):
        return super().build_url('v1/Categories')


@parser_registry.register('catalogue.Category', auto_model=True)
async def parse_category(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('Name', 'Number', 'Path', 'Subcategories',
                                    'IsRestricted', 'HasLegalNotice',
                                    'HasClassifieds', 'AreaOfBusiness'))
    # data now has only the keys we want. And those keys are now snake case.
    data = date_convert(data, 'as_at', 'start_date', 'end_date',
                        'note_date', 'super_feature_end_date')
    data = enum_convert(data, {'area_of_business': enums.AreaOfBusiness})

    data = await parser_convert_lists(data, parser_registry, {
        'subcategories': 'catalogue.Category',
    })
    # Return the data so it can be turned into a model in the registry wrapper.
    return data


class LocalitiesEndpoint(TradeMeApiEndpoint):

    BASE_MODEL_NAME = 'catalogue.Locality'
    EXPECT_LIST = True

    def build_url(self):
        return super().build_url('v1/Localities')


@parser_registry.register('catalogue.Locality', auto_model=True)
async def parse_locality(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('LocalityId', 'Name', 'Districts'))
    # data now has only the keys we want. And those keys are now snake case.
    data = await parser_convert_lists(data, parser_registry, {
        'districts': 'catalogue.District',
    })
    # Return the data so it can be turned into a model in the registry wrapper.
    return data


class DistrictsEndpoint(TradeMeApiEndpoint):

    BASE_MODEL_NAME = 'catalogue.District'
    EXPECT_LIST = True

    def build_url(self, region):
        return super().build_url(['v1/Localities/Region', str(region)])


@parser_registry.register('catalogue.District', auto_model=True)
async def parse_district(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('DistrictId', 'Name', 'Suburbs'))

    data = await parser_convert_lists(data, parser_registry, {
        'suburbs': 'catalogue.Suburb',
    })
    # Return the data so it can be turned into a model in the registry wrapper.
    return data


class SuburbsEndpoint(TradeMeApiEndpoint):

    BASE_MODEL_NAME = 'catalogue.Suburb'
    EXPECT_LIST = True

    def build_url(self, region, district):
        return super().build_url(['v1/Localities/Region',
                                  str(region), str(district)])


@parser_registry.register('catalogue.Suburb', auto_model=True)
def parse_suburb(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('SuburbId', 'Name', 'AdjacentSuburbs'))
    # data now has only the keys we want. And those keys are now snake case.
    if 'adjacent_suburbs' in data:
        adjacent_suburbs = list(data['adjacent_suburbs'])
        if data['suburb_id'] in adjacent_suburbs:
            adjacent_suburbs.remove(data['suburb_id'])
        data['adjacent_suburbs'] = tuple(adjacent_suburbs)
    # Return the data so it can be turned into a model in the registry wrapper.
    return data


class MembershipLocalitiesEndpoint(TradeMeApiEndpoint):

    BASE_MODEL_NAME = 'catalogue.MembershipLocality'
    EXPECT_LIST = True

    def build_url(self):
        return super().build_url('v1/TmAreas')


@parser_registry.register('catalogue.MembershipLocality', auto_model=True)
async def parse_membership_locality(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('LocalityId', 'Name', 'Districts'))
    # data now has only the keys we want. And those keys are now snake case.

    data = await parser_convert_lists(data, parser_registry, {
        'districts': 'catalogue.MembershipDistrict',
    })
    # Return the data so it can be turned into a model in the registry wrapper.
    return data


@parser_registry.register('catalogue.MembershipDistrict', auto_model=True)
def parse_membership_district(json_response, *, parser_registry):
    return reduce_mapping(
        json_response, title_to_snake_case_mapping('DistrictId', 'Name'))


class Manager(APIManagerBase):

    class Endpoints:
        categories = CategoriesEndpoint
        localities = LocalitiesEndpoint
        districts = DistrictsEndpoint
        suburbs = SuburbsEndpoint
        membership_localities = MembershipLocalitiesEndpoint
