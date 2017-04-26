import asyncio

from trademe.api.base import APIManagerBase, TradeMeApiEndpoint
from trademe.api.registry import parser_registry
from trademe.models import enums
from trademe.utils import date_convert, enum_convert, parser_convert_lists
from trademe.utils import parser_convert_singles, reduce_mapping
from trademe.utils import title_to_snake_case_mapping


class ListingEndpoint(TradeMeApiEndpoint):

    BASE_URL = 'https://touch.trademe.co.nz/api/'
    BASE_MODEL_NAME = 'listing.Listing'
    EXPECT_LIST = False

    def build_url(self, listing_id):
        return super().build_url(['v1/Listings', str(listing_id)],
                                 params=dict(
                                     return_member_profile=True,
                                     increment_view_count=False,
        ))


@parser_registry.register('listing.Listing', auto_model=True)
async def parse_listing(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        name_mapping=title_to_snake_case_mapping(
            'Agency', 'AllowsPickups', 'AsAt', 'Attributes',
            'BidderAndWatchers', 'Body', 'BroadbandTechnologies',
            'CanAddToCart', 'Category',
            'EndDate', 'GeographicLocation', 'HasGallery',
            'IsBold', 'IsClassified', 'IsFeatured', 'IsHighlighted',
            'IsSuperFeatured', 'ListingId', 'Member',
            'MemberProfile', 'NoteDate',
            'PhotoId', 'Photos', 'PriceDisplay', 'ShippingOptions', 'StartDate',
            'SuburbId', 'SuperFeatureEndDate', 'Title',
            'ViewingTrackerSupported', 'ViewCount',
            extra={'Suburb': 'suburb_name'}),
        ignore_keys=['ContactDetails', 'CategoryName', 'CategoryPath', 'StartPrice', 
                     'EmbeddedContent', 'SponsorLinks', 'ListingLength',
                     'ReserveState', 'Store', 'ShippingOptions', 'Region',
                     'OpenHomes', 'PaymentOptions', 'StartPrice', 'RegionId'])
    data = date_convert(data, 'as_at', 'start_date', 'end_date',
                        'note_date', 'super_feature_end_date')
    data = enum_convert(data, {'allows_pickups': enums.AllowsPickups})

    data = await parser_convert_singles(data, parser_registry, {
        'agency': 'listing.Agency',
        'geographic_location': 'listing.GeographicLocation',
    })
    data = await parser_convert_lists(data, parser_registry, {
        'attributes': 'listing.Attributes',
        'broadband_technologies': 'listing.BroadbandTechnology',
        'photos': 'listing.Photo',
    })
    if 'member' in data or 'member_profile' in data:
        data['member'] = await parse_listing_member(
            data.pop('member', {}), data.pop('member_profile', {}),
            model_registry=parser_registry.model_registry)
    return data


@parser_registry.register('listing.Agency', auto_model=True)
async def parse_agency(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('Agents', 'Branding', 'FaxNumber', 'Id',
                                    'IsRealEstateAgency', 'Logo', 'Name',
                                    'PhoneNumber', 'Website', 'Logo2',
                                    'IsLicensedPropertyAgency'))
    # De-nest the branding information
    if 'branding' in data:
        branding = data.pop('branding')
        branding = reduce_mapping(
            branding,
            title_to_snake_case_mapping('BackgroundColor', 'LargeBannerURL',
                                        'OfficeLocation', 'StrokeColor',
                                        'TextColor', 'DisableBanner', prefix='branding_'))
        data.update(branding)

    data = await parser_convert_lists(data, parser_registry, {
        'agents': 'listing.AgencyAgent',
    })
    return data


@parser_registry.register('listing.AgencyAgent', auto_model=True)
def parse_agency_agent(json_response, *, parser_registry):
    return reduce_mapping(
        json_response,
        title_to_snake_case_mapping('FullName', 'MobilePhoneNumber',
                                    'OfficePhoneNumber', 'Photo', 'UrlSlug'))


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


async def parse_listing_member(member, member_profile, *, model_registry):
    member = member or {}
    member_profile = member_profile or {}
    profile = {}
    profile.update(reduce_mapping(
        member,
        title_to_snake_case_mapping('DateAddressVerified', 'DateJoined',
                                    'Suburb', 'Nickname', 'UniquePositive',
                                    'Region', 'IsAddressVerified',
                                    'IsAuthenticated', 'UniqueNegative',
                                    'FeedbackCount', 'MemberId', 'IsInTrade'
                                    ),
        ignore_keys=['ImportChargesMayApply']))
    profile.update(reduce_mapping(
        member_profile,
        title_to_snake_case_mapping('Biography', 'Photo', 'Occupation', 'Quote'
                                    )))
    profile = date_convert(profile, 'date_joined', 'date_address_verified')
    return await model_registry.get_model('listing.Member')(profile)


@parser_registry.register('listing.Member', auto_model=True)
def parse_member(json_response, *, parser_registry):
    profile = {}
    member_info_keys = ()
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
            title_to_snake_case_mapping()))
    profile = date_convert(profile, 'date_joined', 'date_address_verified')
    return profile


@parser_registry.register('listing.Photo', auto_model=True)
def parse_photo(json_response, *, parser_registry):
    return reduce_mapping(
        json_response['Value'],
        title_to_snake_case_mapping('FullSize', 'Gallery', 'Large', 'List',
                                    'Medium', 'PhotoId', 'PlusSize',
                                    'Thumbnail'))


class ViewingTimesEndpoint(TradeMeApiEndpoint):
    BASE_URL = 'https://preview.trademe.co.nz/ngapi/'
    BASE_MODEL_NAME = 'listing.ViewingTimes'
    EXPECT_LIST = False

    def build_url(self, listing_id):
        return super().build_url(['v1/property/viewingtracker/',
                                 str(listing_id), '/availableviewingtimes'])


@parser_registry.register('listing.ViewingTimes')
async def parse_viewing_times(json_response, *,
                              parser_registry, model_registry):
    vt_parser = parser_registry.get_parser('listing.ViewingTime')
    viewing_times = []
    for viewing_time in json_response.get('AvailableViewingTimes', {}).values():
        viewing_times.append(vt_parser(viewing_time))
    return await asyncio.gather(*viewing_times)


@parser_registry.register('listing.ViewingTime', auto_model=True)
def parse_viewing_time(json_response, *, parser_registry):
    data = reduce_mapping(
        json_response,
        title_to_snake_case_mapping('ViewingId', 'ViewingTime'))
    data = date_convert(data, 'viewing_time')
    return data


class Manager(APIManagerBase):

    class Endpoints:
        listing = ListingEndpoint
        viewing_times = ViewingTimesEndpoint
