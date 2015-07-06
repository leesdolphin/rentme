import rentme_web.models as models
from django.utils.timezone import utc
import trademe.api as api
from requests.structures import CaseInsensitiveDict
import re
from datetime import datetime, tzinfo

TRADEME_DATE_REGEX = re.compile(r'^/Date\(([0-9]+)\)/$')

def load_trademe_locality_information():
    session = api.API()
    adj_suburbs = {}
    ## Array
    localities = session.get_localities()
    for locality in localities:
        l_name = locality["Name"]
        l_id = locality["LocalityId"]
        l, _ = models.TradeMeLocality.objects.get_or_create(id=l_id,
                                                            name=l_name)
        print(l)
        for districts in locality["Districts"]:
            d_name = districts["Name"]
            d_id = districts["DistrictId"]
            d, _ = models.TradeMeDistrict.objects.get_or_create(id=d_id,
                                                                name=d_name,
                                                                locality=l)
            for suburb in districts["Suburbs"]:
                s_name = suburb["Name"]
                s_id = suburb["SuburbId"]
                s, _ = models.TradeMeSuburb.objects.get_or_create(id=s_id,
                                                                  name=s_name,
                                                                  district=d)
                adj_suburbs[s] = suburb.get("AdjacentSuburbs", [])
    ## All suburbs added, now handle adjacency.
    for suburb, adj_list in adj_suburbs.items():
        suburb.adjacent_suburbs = models.TradeMeSuburb.objects\
                                        .filter(id__in=adj_list).all()
    return localities

def search_rentals(**kwargs):
    ## TODO create suburbs string
    params = CaseInsensitiveDict(kwargs)
    params.setdefault('page', 1)
    params.setdefault('rows', 100)
    params.setdefault('photo_size', 'FullSize')
    rows = params['rows'] = int(params['rows'])
    session = api.API()
    more_pages = True
    listings = []
    while more_pages:
        print("Params:", params)
        rentals = session.search_rental(params)
        for listing_data in rentals['List']:
            get = listing_data.get
            ## This loads preliminary data. It is sufficient to display; but
            ##  full data should be loaded before displaying individual listing.
            try:
                listing = models.TradeMeListing.objects.get(
                    id=get('ListingId'))
                load_rental(get('ListingId'))
                continue  ## In the DB; assume up to date.
            except models.TradeMeListing.DoesNotExist:
                listing = models.TradeMeListing()
                listing.id = get('ListingId')
                listing.generated_at = _d(get('AsAt'))
            listing.title = get('Title')
            listing.category = get('Category', None)
            listing.address = get('Address', None)
            listing.thumbnail_href = get('PictureHref')
            listing.available_from = get('AvailableFrom')
            listing.bathrooms = get('Bathrooms')
            listing.bedrooms = get('Bedrooms')
            listing.start_date = _d(get('StartDate'))
            listing.end_date = _d(get('EndDate'))
            listing.rent_per_week = get('RentPerWeek')
            listing.location = get_location(get('GeographicLocation'))
            listing.save()
            listing.agency = get_agency(get('Agency'))
            listing.save()
            ## Reduce the save size to speed up updates.
            listing.generated_at = _d(get('AsAt'))
            listing.save()
            load_rental(get('ListingId'))
            listings.append(listing)
        params['page'] = rentals["Page"] + 1
        more_pages = (rentals["PageSize"] >= rows)
    return listings


def _d(trademe_date_string):
    time_str = TRADEME_DATE_REGEX.match(trademe_date_string).group(1)
    return datetime.fromtimestamp(int(time_str) / 1000, utc)


def get_agency(agency_data):
    if not agency_data:
        return []
    get = agency_data.get
    try:
        agency = models.TradeMeAgency.objects.get(id=get("Id"))
    except models.TradeMeAgency.DoesNotExist:
        agency = models.TradeMeAgency(id=get("Id"))

    agency.logo = get('Logo', None)
    agency.name = get('Name')
    agency.phone_number = get('PhoneNumber', None)
    agency.website = get('Website', None)
    agency.is_real_estate_agency = get('IsRealEstateAgency', False)
    agency.is_licensed_property_agency = get('IsRealEstateAgency', False)
    agency.save()

    for agent_data in get('Agents', []):
        name = agent_data.get('FullName')
        try:
            agent = models.TraceMeAgencyAgent.objects.get(agency=agency,
                                                          full_name=name)
        except models.TraceMeAgencyAgent.DoesNotExist:
            agent = models.TraceMeAgencyAgent(agency=agency, full_name=name)
        agent.position = agent_data.get('Position', None)
        agent.mobile_number = agent_data.get('MobilePhoneNumber', None)
        agent.office_number = agent_data.get('OfficePhoneNumber', None)
        agent.email = agent_data.get('EMail', None)
        agent.fax_number = agent_data.get('FaxNumber', None)
        agent.save()
    agency.save()
    return [agency]


def get_location(location_data):
    return models.TradeMeListingLocation.objects.get_or_create(
        latitude=location_data["Latitude"],
        longitude=location_data["Longitude"],
        accuracy=location_data["Accuracy"],
    )[0]


def get_attributes(listing, attrs):
    for attr_data in attrs:
        get = attr_data.get
        try:
            attr = listing.attributes.get(name=get('Name'))
        except models.TradeMeListingAttribute.DoesNotExist:
            attr = models.TradeMeListingAttribute()
            attr.name = get('Name')
        attr.display_name = get('DisplayName')
        attr.value = get('Value')


def get_photos(photos_data):
    photos = []
    for photo_data in photos_data:
        get = photo_data.get('Value', {}).get
        try:
            photo = models.TradeMeListingPhoto.objects.get(
                id=photo_data.get('Key'))
        except models.TradeMeListingPhoto.DoesNotExist:
            photo = models.TradeMeListingPhoto()
            photo.id = photo_data.get('Key')
        photo.thumbnail = get('Thumbnail')
        photo.list = get('List')
        photo.medium = get('Medium')
        photo.gallery = get('Gallery')
        photo.large = get('Large')
        photo.full_size = get('FullSize')
        photo.plus_size = get('PlusSize')
        photo.original_width = get('OriginalWidth', -1)
        photo.original_height = get('OriginalHeight', -1)
        print(photo_data.get('Key'), get('PhotoId'), photo)
        photo.save()
        photos.append(photo)
    return photos


def get_member(member):
    return None


def load_rental(id):
    try:
        listing = models.TradeMeListing.objects.get(
            id=int(id))
        if listing.description:
            return listing  ## Has a body, don't need to update again.
    except models.TradeMeListing.DoesNotExist:
        listing = models.TradeMeListing()
        listing.id = int(id)
    session = api.API()
    info = session.get_rental(id, {'return_member_profile': True})
    print(info)
    get = info.get
    listing.generated_at = _d(get('AsAt'))
    listing.title = get('Title')
    listing.category = get('Category', None)
    listing.description = get('Body')
    listing.start_date = _d(get('StartDate'))
    listing.end_date = _d(get('EndDate'))
    listing.location = get_location(get('GeographicLocation'))
    listing.photos = get_photos(get('Photos'))
    listing.member = get_member(get('Member'))
    listing.save()
    listing.agency = get_agency(get('Agency'))
    get_attributes(listing, get('Attributes'))
    listing.save()
    ## Reduce the save size to speed up updates.
    listing.generated_at = _d(get('AsAt'))
    listing.save()
    return listing







