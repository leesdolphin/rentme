from aioutils.celery import asyncio_task, delay_or_call
from celery.utils.log import get_task_logger
from django.db import transaction

from rentme.celery.celery_app import app
from rentme.raw.models.search import Property, Flatmate
from rentme.raw.models.listings import ListedItemDetail
from ._utils import migrate_model, migrate_merge_model
from .error import ModelDataMissing
from rentme.data.models import listings, catalogue, members


logger = get_task_logger(__name__)


@asyncio_task(app, ignore_result=True, rate_limit='5/s')
@transaction.atomic
async def migrate_listing(listing_id, *, loop):
    old_listing = ListedItemDetail.objects.get(listing_id=listing_id)
    try:
        search_listing = Property.objects.get(listing_id=listing_id)
        flatmate_info = None
        listing_type = listings.ListingType.PROPERTY
    except Property.DoesNotExist:
        try:
            search_listing = Flatmate.objects.get(listing_id=listing_id)
        except Flatmate.DoesNotExist:
            await delete_listing(listing_id)
            return
        flatmate_info, _ = listings.FlatmateInformation.objects.get_or_create(
            current_flatmates=search_listing.current_flatmates,
            flatmates=search_listing.flatmates,
        )
        listing_type = listings.ListingType.FLATMATE

    broadband_techs = migrate_broadband_technologies(
        old_listing.broadband_technologies.all())
    photos = migrate_photos(old_listing.photos.all())
    agency = migrate_agency(old_listing.agency)
    geo = migrate_geolocation(old_listing.geographic_location)
    embedded_content = migrate_embedded_content(old_listing.embedded_content)
    photo = try_get(listings.Photo, photo_id=old_listing.photo_id)
    category = try_get(catalogue.Category, path=old_listing.category_path)
    suburb = try_get(catalogue.Suburb, suburb_id=old_listing.suburb_id)
    member = try_get(members.Member, member_id=old_listing.member.member_id)

    new_listing = migrate_merge_model(
        [search_listing, old_listing],
        listings.Listing,
        agency=agency,
        geographic_location=geo,
        embedded_content=embedded_content,
        flatmate_information=flatmate_info,
        listing_type=listing_type,
        photo=photo,
        category=category,
        suburb=suburb,
        member=member,
    )
    new_listing.broadband_technologies.set(broadband_techs)
    new_listing.photos.set(photos)
    update_attributes(new_listing, old_listing.attributes.all())
    new_listing.save()
    return new_listing


def try_get(model, **lookup):
    if not lookup or all(v is None for v in lookup.values()):
        return None
    try:
        return model.objects.get(**lookup)
    except model.DoesNotExist:
        return None


def update_attributes(new_listing, old_attrs):
    attr_name_to_listing = {
        'current_flatmates': None,
        'district': None,
        'maximum_tenants': None,
        'pets_and_smokers': None,
        'price': None,
        'region': None,
        'rooms': None,
        'suburb': None,
        'agency_reference_#': 'agency_reference',
        'avaliable': 'available_from',
        'furnishings': 'whiteware',
        'ideal_flatmates': 'ideal_tenant',
        'ideal_tenants': 'ideal_tenant',
        'in_the_area': 'amenities',
        'location': 'address',
        'parking': 'parking',
        'property_id': 'property_id',
    }
    renamed = {
        name: new_name
        for name, new_name in attr_name_to_listing.items()
        if new_name is not None
    }
    new_attrs = migrate_attrs(
        old_attrs,
        exclude=attr_name_to_listing.keys())
    attr_map = {a.name: a.value for a in old_attrs}
    for attr_name, new_name in renamed.items():
        if attr_name in attr_map:
            setattr(new_listing, new_name, attr_map[attr_name])
    new_listing.attributes.set(new_attrs)
    return new_attrs


def migrate_agency(old_agency):
    if not old_agency:
        return None
    new_branding = migrate_branding(old_agency.branding)
    new_agency = migrate_model(
        old_agency,
        listings.Agency,
        branding=new_branding,
    )
    for old_agent in old_agency.agents.all():
        migrate_agent(old_agent, new_agency=new_agency)
    return new_agency


def migrate_agent(old_agent, *, new_agency):
    new_agent = migrate_model(
        old_agent,
        listings.Agent,
        agency=new_agency,
    )
    return new_agent


def migrate_attrs(old_attrs, *, exclude=()):
    new_attrs = []
    for old_attr in old_attrs:
        if old_attr.name in exclude:
            continue
        new_attr = migrate_model(
            old_attr,
            listings.Attribute,
        )
        new_attrs.append(new_attr)
    return new_attrs


def migrate_branding(old_branding):
    new_branding = migrate_model(
        old_branding,
        listings.Branding,
    )
    return new_branding


def migrate_broadband_technologies(old_broadband_techs):
    new_techs = []
    for old_broadband in old_broadband_techs:
        new_broadband = migrate_model(
            old_broadband,
            listings.BroadbandTechnology,
        )
        new_techs.append(new_broadband)
    return new_techs


def migrate_embedded_content(old_embedded_content):
    new_embedded_content = migrate_model(
        old_embedded_content,
        listings.EmbeddedContent,
    )
    return new_embedded_content


def migrate_geolocation(old_geolocation):
    new_geo = migrate_model(
        old_geolocation,
        listings.GeographicLocation,
    )
    return new_geo


def migrate_member(old_member):
    new_member = migrate_model(
        old_member,
        members.Member,
    )
    return new_member


def migrate_photo(old_photo):
    new_photo = migrate_model(
        old_photo,
        listings.Photo,
    )
    return new_photo


def migrate_photos(old_photos):
    new_photos = []
    for old_photo in old_photos:
        new_photo = migrate_photo(old_photo)
        new_photos.append(new_photo)
    return new_photos


async def delete_listing(listing_id):
    from ..listing import delete_listing
    return await delay_or_call(delete_listing, listing_id)
