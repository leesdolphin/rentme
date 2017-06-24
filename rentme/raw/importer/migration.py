import math

from aioutils.celery import asyncio_task, delay_or_call
from aioutils.task_queues import SizeBoundedTaskList
from celery.utils.log import get_task_logger
from trademe.errors import ClassifiedExpiredError

from rentme.celery.celery_app import app
from rentme.raw.api import get_trademe_api
from rentme.raw.models.search import Property, Flatmate
from rentme.data.models import listings
# from rentme.raw.models.detail import ListedItemDetail


logger = get_task_logger(__name__)


@asyncio_task(app, ignore_result=True, rate_limit='1/m')
async def migrate_listing(listing_id, *, loop):
    listing = ListedItemDetail.objects.get(listing_id)
    try:
        search_listing = Property.objects.get(listing_id)
        is_property = True
    except Property.DoesNotExist:
        search_listing = Flatmate.objects.get(listing_id)
        is_property = False
    attributes = migrate_attrs(listing.attributes.all())
    geo = migrate_geolocation(listing.geographic_location)


def migrate_agency(old_agency):
    if not old_agency:
        return None
    new_branding = migrate_branding(old_agency.branding)
    new_agency, _ = listings.Agency.objects.update_or_create(
        id=old_agency.id,
        defaults=dict(
            address=old_agency.address,
            branding=new_branding,
            city=old_agency.city,
            e_mail=old_agency.e_mail,
            fax_number=old_agency.fax_number,
            id=old_agency.id,
            is_job_agency=old_agency.is_job_agency,
            is_licensed_property_agency=old_agency.is_licensed_property_agency,
            is_real_estate_agency=old_agency.is_real_estate_agency,
            logo=old_agency.logo,
            logo2=old_agency.logo2,
            name=old_agency.name,
            phone_number=old_agency.phone_number,
            suburb=old_agency.suburb,
            website=old_agency.website,
        )
    )
    for old_agent in old_agency.agents.all():
        migrate_agent(old_agent, new_agency=new_agency)
    return new_agency


def migrate_agent(old_agent, *, new_agency):
    new_agent, _ = listings.Agent.objects.update_or_create(
        agency=new_agency,
        e_mail=old_agent.e_mail,
        fax_number=old_agent.fax_number,
        full_name=old_agent.full_name,
        home_phone_number=old_agent.home_phone_number,
        mobile_phone_number=old_agent.mobile_phone_number,
        office_phone_number=old_agent.office_phone_number,
        photo=old_agent.photo,
        position=old_agent.position,
        url_slug=old_agent.url_slug,
    )
    return new_agent


def migrate_attrs(old_attrs, *, exclude=()):
    new_attrs = []
    for old_attr in old_attrs:
        if old_attr.name in exclude:
            continue
        new_attr = listings.Attribute.objects.update_or_create(
            name=old_attr.name,
            value=old_attr.value,
            defaults=dict(
                display_name=old_attr.display_name,
                display_value=old_attr.display_value,
            )
        )
        new_attrs.append(new_attr)
    return new_attrs


def migrate_branding(old_branding):
    new_branding, _ = listings.Branding.objects.update_or_create(
        background_color=old_branding.background_color,
        disable_banner=old_branding.disable_banner,
        large_banner_url=old_branding.large_banner_url,
        large_square_logo=old_branding.large_square_logo,
        large_wide_logo=old_branding.large_wide_logo,
        office_location=old_branding.office_location,
        stroke_color=old_branding.stroke_color,
        text_color=old_branding.text_color,
    )
    return new_branding


def migrate_broadband_technology(old_broadband):
    new_broadband, _ = listings.GeographicLocation.objects.update_or_create(
        availability=old_broadband.availability,
        completion=old_broadband.completion,
        max_down=old_broadband.max_down,
        max_up=old_broadband.max_up,
        min_down=old_broadband.min_down,
        min_up=old_broadband.min_up,
        name=old_broadband.name,
    )
    return new_broadband


def migrate_geolocat(old_geolocation):
    new_geo, _ = listings.GeographicLocation.objects.update_or_create(
        accuracy=old_geolocation.accuracy,
        latitude=old_geolocation.latitude,
        longitude=old_geolocation.longitude,
    )
    return new_geo


def migrate_member(old_member):
    new_geo, _ = listings.GeographicLocation.objects.update_or_create(
        accuracy=old_geolocation.accuracy,
        latitude=old_geolocation.latitude,
        longitude=old_geolocation.longitude,
    )
    return new_geo
