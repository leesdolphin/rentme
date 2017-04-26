from celery.utils.log import get_task_logger
from django.db import transaction
from django.db.models import Q

from rentme.data.importer.celery import app
from rentme.data.importer.utils import asyncio_task, get_trademe_api
from rentme.data.models.catalogue import District, Locality, Suburb


logger = get_task_logger(__name__)


@asyncio_task(app)
async def reload_categories():
    async with get_trademe_api() as api:
        categories = await api.catalogue.categories()
    return len(categories)


@asyncio_task(app, ignore_result=True)
async def reload_localities(*, _loop):
    async with get_trademe_api(db_models=False) as api:
        localities = await api.catalogue.localities()
    await _loop.run_in_executor(None, save_and_clean_localities, localities)


def save_and_clean_localities(localities):
    with transaction.atomic():
        db_localities = save_localities(localities)

        locality_ids = [l.locality_id for l in db_localities]
        Locality.objects.filter(~Q(locality_id__in=locality_ids)).delete()
        District.objects.filter(~Q(locality__in=locality_ids)).delete()
        Suburb.objects.filter(~Q(district__locality__in=locality_ids)).delete()


def save_localities(localities):
    suburb_adjacency = {}
    suburbs_by_id = {}
    db_localities = []
    for locality in localities:
        db_locality, _ = Locality.objects.update_or_create(
            locality_id=locality.locality_id,
            defaults=dict(name=locality.name))
        db_districts = []
        for district in locality.districts:
            db_district, _ = District.objects.update_or_create(
                district_id=district.district_id,
                defaults=dict(name=district.name))
            db_suburbs = []
            for suburb in district.suburbs:
                db_suburb, _ = Suburb.objects.update_or_create(
                    suburb_id=suburb.suburb_id,
                    defaults=dict(name=suburb.name))
                db_suburb.save()
                suburb_adjacency[db_suburb.suburb_id] = suburb.adjacent_suburbs
                suburbs_by_id[db_suburb.suburb_id] = db_suburb
                db_suburbs.append(db_suburb)
            db_district.suburbs.set(db_suburbs, clear=True)
            db_district.save()
            db_districts.append(db_district)
        db_locality.districts.set(db_districts, clear=True)
        db_locality.save()
        db_localities.append(db_locality)
    for sid, adjacent_ids in suburb_adjacency.items():
        db_suburb = suburbs_by_id[sid]
        adj_db_suburbs = []
        for adj_id in adjacent_ids:
            if adj_id in suburbs_by_id:
                adj_db_suburb = suburbs_by_id[adj_id]
                adj_db_suburbs.append(adj_db_suburb)
            else:
                logger.warning('Adjacent suburb does not exist. '
                               'From: %s to %s',
                               sid, adj_id)
        db_suburb.adjacent_suburbs.set(adj_db_suburbs, clear=True)
    return db_localities


@asyncio_task(app)
async def reload_membership_localities():
    async with get_trademe_api() as api:
        membership_localities = await api.catalogue.membership_localities()
    return len(membership_localities)
