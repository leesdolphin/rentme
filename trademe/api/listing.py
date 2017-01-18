from trademe.api.base import APIManagerBase, TradeMeApiEndpoint
from trademe.api.registry import parser_registry
from trademe.utils import date_convert_many, enum_convert_many, reduce_mapping, title_to_snake_case_mapping
from trademe.models import enums

class ListingEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://touch.trademe.co.nz/api/'
    BASE_MODEL_NAME = 'listing.Listing'
    EXPECT_LIST = False

    def build_url(self, listing_id, *kwargs):
        return super().build_url(['v1/Listings', str(listing_id)],
                                 params=dict(return_member_profile=True))


@parser_registry.register('listing.Listing', auto_model=True)
def parse_listing(json_response, *, parser_registry):
    # print(json_response['ContactDetails'])
    data = reduce_mapping(
        json_response,
        name_mapping=title_to_snake_case_mapping(
            'Agency', 'AllowsPickups', 'AsAt', 'Attributes',
            'BidderAndWatchers', 'Body', 'BroadbandTechnologies',
            'CanAddToCart', 'Category', 'CategoryName', 'CategoryPath', 'ContactDetails',
            'EmbeddedContent', 'EndDate', 'GeographicLocation', 'HasGallery',
            'IsBold', 'IsClassified', 'IsFeatured', 'IsHighlighted',
            'IsSuperFeatured', 'ListingId', 'ListingLength', 'Member',
            'MemberProfile', 'NoteDate', 'OpenHomes', 'PaymentOptions',
            'PhotoId', 'Photos', 'Photos', 'PriceDisplay', 'Region',
            'RegionId', 'ReserveState', 'ShippingOptions', 'StartDate',
            'StartPrice', 'Suburb', 'SuburbId', 'SuperFeatureEndDate', 'Title',
            'ViewingTrackerSupported', 'ViewCount'),
        ignore_keys=['SponsorLinks'])
    data = date_convert_many(data, 'as_at', 'start_date', 'end_date', 'note_date')
    data = enum_convert_many(data, {'allows_pickups': enums.AllowsPickups})
    if 'agency' in data:
        agency_parser = parser_registry.get_parser('listing.Agency')
        data['agency'] = agency_parser(data['agency'])
    if 'attributes' in data:
        bt_parser = parser_registry.get_parser('listing.Attributes')
        attrs = []
        for attr in data['attributes']:
            attrs.append(bt_parser(attr))
        data['attributes'] = attrs
    if 'broadband_technologies' in data:
        bt_parser = parser_registry.get_parser('listing.BroadbandTechnology')
        techs = []
        for tech in data['broadband_technologies']:
            techs.append(bt_parser(tech))
        data['broadband_technologies'] = techs
    if 'geographic_location' in data:
        geo_parser = parser_registry.get_parser('listing.GeographicLocation')
        data['geographic_location'] = geo_parser(data['geographic_location'])
    if 'member' in data or 'member_profile' in data:
        member_info = {}
        if 'member' in data:
            member_info.update(data['member'])
        if 'member_profile' in data:
            member_info.update(data['member_profile'])
            del data['member_profile']
        member_parser = parser_registry.get_parser('listing.Member')
        data['member'] = member_parser(member_info)
    if 'photos' in data:
        photo_parser = parser_registry.get_parser('listing.Photo')
        photos = []
        for photo in data['photos']:
            photos.append(photo_parser(photo))
        data['photos'] = photos
    return data


@parser_registry.register('listing.Agency', auto_model=True)
def parse_agency(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('Agents', 'Branding', 'FaxNumber', 'Id',
                                    'IsRealEstateAgency', 'Logo', 'Name',
                                    'PhoneNumber', 'Website'))
    # De-nest the branding information
    if 'branding' in data:
        branding = data.pop('branding')
        branding = reduce_mapping(
            branding,
            title_to_snake_case_mapping('BackgroundColor', 'LargeBannerURL',
                                        'OfficeLocation', 'StrokeColor',
                                        'TextColor', prefix='branding_'))
        data.update(branding)
    if 'agents' in data:
        mapped_agents = []
        agent_parser = parser_registry.get_parser('listing.AgencyAgent')
        for agent in data['agents']:
            mapped_agents.append(agent_parser(agent))
        data['agents'] = mapped_agents
    return data


@parser_registry.register('listing.AgencyAgent', auto_model=True)
def parse_agency_agent(json_response, *, parser_registry):
    return reduce_mapping(
        json_response,
        title_to_snake_case_mapping('FullName', 'MobilePhoneNumber',
                                    'OfficePhoneNumber'))


@parser_registry.register('listing.Attributes', auto_model=True)
def parse_attributes(json_response, *, parser_registry):
    return reduce_mapping(
        json_response,
        title_to_snake_case_mapping('DisplayName', 'Name',
                                    'Value'))


@parser_registry.register('listing.BroadbandTechnology', auto_model=True)
def parse_broadband_technology(json_response, *, parser_registry):
    return reduce_mapping(
        json_response,
        title_to_snake_case_mapping('Availability', 'Completion', 'MaxDown',
                                    'MaxUp', 'MinDown', 'MinUp', 'Name'))


@parser_registry.register('listing.GeographicLocation', auto_model=True)
def parse_geographic_location(json_response, *, parser_registry):
    return reduce_mapping(
        json_response,
        title_to_snake_case_mapping('Accuracy', 'Easting', 'Latitude', 'Longitude', 'Northing'))


@parser_registry.register('listing.Member', auto_model=True)
def parse_member(json_response, *, parser_registry):
    profile = {}
    member_info_keys = ('DateAddressVerified', 'DateJoined', 'FeedbackCount',
                        'IsAddressVerified', 'IsAuthenticated', 'MemberId',
                        'Nickname', 'Region', 'Suburb', 'UniqueNegative',
                        'UniquePositive', 'Photo')
    if 'MemberId' in json_response:
        profile.update(reduce_mapping(
            json_response,
            title_to_snake_case_mapping(*member_info_keys)))
    if 'Member' in json_response:
        profile.update(reduce_mapping(
            json_response['Member'],
            title_to_snake_case_mapping(*member_info_keys)))
    if 'Biography' in json_response:
        profile.update(reduce_mapping(
            json_response,
            title_to_snake_case_mapping('Biography', 'FirstName', 'Occupation',
                                        'Photo', 'Quote')))
    profile = date_convert_many(profile, 'date_joined', 'date_address_verified')
    return profile


@parser_registry.register('listing.Photo', auto_model=True)
def parse_photo(json_response, *, parser_registry):
    return reduce_mapping(
        json_response['Value'],
        title_to_snake_case_mapping('FullSize', 'Gallery', 'Large', 'List',
                                    'Medium', 'PhotoId', 'PlusSize',
                                    'Thumbnail'))


class Manager(APIManagerBase):

    class Endpoints:
        listing = ListingEndpoint
