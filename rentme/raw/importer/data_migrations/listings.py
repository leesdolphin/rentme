from pprint import pprint

from aioutils.celery import asyncio_task, delay_or_call
from celery.utils.log import get_task_logger
from django.db import transaction

from rentme.celery.celery_app import app
from rentme.raw.models.search import Property, Flatmate
from rentme.raw.models.listings import ListedItemDetail
from ._utils import migrate_model, migrate_merge_model, model_to_dict
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

    broadband_techs = await migrate_broadband_technologies(
        old_listing.broadband_technologies.all())
    photos = await migrate_photos(old_listing.photos.all())
    agency = await migrate_agency(old_listing.agency)
    geo = await migrate_geolocation(old_listing.geographic_location)
    embedded_content = await migrate_embedded_content(
        old_listing.embedded_content
    )
    photo = await try_get(listings.Photo, photo_id=old_listing.photo_id)
    category = await try_get(
        catalogue.Category,
        path=old_listing.category_path
    )
    suburb_by_id = await try_get(
        catalogue.Suburb,
        suburb_id=old_listing.suburb_id,
        district__district_id=old_listing.region_id
    )
    suburb_by_name = await try_get(
        catalogue.Suburb,
        name=old_listing.suburb,
        district__name=old_listing.region
    )
    member = await try_get(
        members.Member,
        member_id=old_listing.member.member_id
    )

    if suburb_by_name is None and suburb_by_id is None:
        print("Cannot find suburb: ", dict(
            suburb_id=old_listing.suburb_id,
            suburb_name=old_listing.suburb,
            district_id=old_listing.region_id,
            district_name=old_listing.region
        ))
        suburb = None
    elif suburb_by_name is not None:
        suburb = suburb_by_name
    else:
        suburb = suburb_by_id

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


async def try_get(model, **lookup):
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


async def migrate_agency(old_agency):
    if not old_agency:
        return None
    new_branding = await migrate_branding(old_agency.branding)
    new_agency = migrate_model(
        old_agency,
        listings.Agency,
        branding=new_branding,
    )
    for old_agent in old_agency.agents.all():
        await migrate_agent(old_agent, new_agency=new_agency)
    return new_agency


async def migrate_agent(old_agent, *, new_agency):
    new_agent = migrate_model(
        old_agent,
        listings.Agent,
        agency=new_agency,
    )
    return new_agent


async def migrate_attrs(old_attrs, *, exclude=()):
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


async def migrate_branding(old_branding):
    new_branding = migrate_model(
        old_branding,
        listings.Branding,
    )
    return new_branding


async def migrate_broadband_technologies(old_broadband_techs):
    new_techs = []
    for old_broadband in old_broadband_techs:
        new_broadband = migrate_model(
            old_broadband,
            listings.BroadbandTechnology,
        )
        new_techs.append(new_broadband)
    return new_techs


async def migrate_embedded_content(old_embedded_content):
    new_embedded_content = migrate_model(
        old_embedded_content,
        listings.EmbeddedContent,
    )
    return new_embedded_content


async def migrate_geolocation(old_geolocation):
    new_geo = migrate_model(
        old_geolocation,
        listings.GeographicLocation,
    )
    return new_geo


async def migrate_member(old_member):
    new_member = migrate_model(
        old_member,
        members.Member,
    )
    return new_member


def migrate_photo(old_photo):
    if old_photo.photo_id == 0:
        return None
    new_photo = migrate_merge_model(
        [old_photo.value, old_photo],
        listings.Photo,
    )
    if new_photo.full_size is None:
        print("Old Value, Old, New")
        pprint(model_to_dict(old_photo.value))
        pprint(model_to_dict(old_photo))
        pprint(model_to_dict(new_photo))
    return new_photo


async def migrate_photos(old_photos):
    new_photos = []
    for old_photo in old_photos:
        new_photo = migrate_photo(old_photo)
        if new_photo:
            new_photos.append(new_photo)
    return new_photos


async def delete_listing(listing_id):
    from ..listing import delete_listing
    return await delay_or_call(delete_listing, listing_id)
