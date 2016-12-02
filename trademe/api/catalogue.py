from trademe.api.base import TradeMeApiEndpoint
from trademe.api.base_parsers import parser_registry, simple_rename_parser
from trademe.models import enums
from trademe.utils import title_to_snake_case_mapping, reduce_mapping


class CategoriesEndpoint(TradeMeApiEndpoint):

    BASE_MODEL_NAME = 'catalogue.Category'
    EXPECT_LIST = True

    def build_url(self):
        return super().build_url('v1/Categories')


@parser_registry.register('catalogue.Category', auto_model=True)
def parse_category(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('Name', 'Number', 'Path', 'Subcategories',
                                    'IsRestricted', 'HasLegalNotice',
                                    'HasClassifieds', 'AreaOfBusiness'))
    # data now has only the keys we want. And those keys are now snake case.
    if 'area_of_business' in data:
        data['area_of_business'] = enums.AreaOfBusiness(data['area_of_business'])
    if 'subcategories' in data:
        subcats = []
        parser = parser_registry.get_parser('catalogue.Category')
        for subcat in data['subcategories']:
            subcats.append(parser(subcat))
        data['subcategories'] = subcats
    # Return the data so it can be turned into a model in the registry wrapper.
    return data


class LocalitiesEndpoint(TradeMeApiEndpoint):

    BASE_MODEL_NAME = 'catalogue.Locality'
    EXPECT_LIST = True

    def build_url(self):
        return super().build_url('v1/Localities')


@parser_registry.register('catalogue.Locality', auto_model=True)
def parse_locality(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('LocalityId', 'Name', 'Districts'))
    # data now has only the keys we want. And those keys are now snake case.
    if 'districts' in data:
        districts = []
        parser = parser_registry.get_parser('catalogue.District')
        for district in data['districts']:
            districts.append(parser(district))
        data['districts'] = districts
    # Return the data so it can be turned into a model in the registry wrapper.
    return data


class DistrictsEndpoint(TradeMeApiEndpoint):

    BASE_MODEL_NAME = 'catalogue.District'
    EXPECT_LIST = True

    def build_url(self, region):
        return super().build_url(['v1/Localities/Region', str(region)])


@parser_registry.register('catalogue.District', auto_model=True)
def parse_district(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('DistrictId', 'Name', 'Suburbs'))
    # data now has only the keys we want. And those keys are now snake case.
    if 'suburbs' in data:
        suburbs = []
        parser = parser_registry.get_parser('catalogue.Suburb')
        for suburb in data['suburbs']:
            suburbs.append(parser(suburb))
        data['suburbs'] = suburbs
    # Return the data so it can be turned into a model in the registry wrapper.
    return data


class SuburbsEndpoint(TradeMeApiEndpoint):

    BASE_MODEL_NAME = 'catalogue.Suburb'
    EXPECT_LIST = True

    def build_url(self, region, district):
        return super().build_url(['v1/Localities/Region',
                                  str(region), str(district)])


@parser_registry.register('catalogue.Suburb')
def parse_suburb(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('SuburbId', 'Name', 'AdjacentSuburbs'))
    # data now has only the keys we want. And those keys are now snake case.
    if 'adjacent_suburbs' in data:
        data['adjacent_suburbs'] = tuple(data['adjacent_suburbs'])
    # Return the data so it can be turned into a model in the registry wrapper.
    return data


class MembershipLocalitiesEndpoint(TradeMeApiEndpoint):

    BASE_MODEL_NAME = 'catalogue.MembershipLocality'
    EXPECT_LIST = True

    def build_url(self, region, district):
        return super().build_url('v1/TmAreas')


@parser_registry.register('catalogue.MembershipLocality', auto_model=True)
def parse_membership_locality(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('LocalityId', 'Name', 'Districts'))
    # data now has only the keys we want. And those keys are now snake case.
    if 'districts' in data:
        districts = []
        parser = parser_registry.get_parser('catalogue.MembershipDistrict')
        for district in data['districts']:
            districts.append(parser(district))
        data['districts'] = districts
    # Return the data so it can be turned into a model in the registry wrapper.
    return data


@parser_registry.register('catalogue.MembershipDistrict', auto_model=True)
def parse_membership_district(json_response, *, parser_registry):
    return reduce_mapping(
        json_response, title_to_snake_case_mapping('DistrictId', 'Name'))


# https://api.trademe.co.nz/v1/Search/Property/Rental.
