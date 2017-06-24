from aioutils.celery import asyncio_task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.db.models import Q

from rentme.celery.celery_app import app
from rentme.raw.api import get_trademe_api
from rentme.data.models import catalogue


logger = get_task_logger(__name__)


@asyncio_task(app, ignore_result=True)
@transaction.atomic
async def reload_categories(*, loop):
    async with get_trademe_api(loop=loop) as api:
        root_category = await api.catalogue.categories()
    query = Q(parent=None) & ~Q(pk=root_category.pk)
    count, deleted = catalogue.Category.objects.filter(query).delete()


@asyncio_task(app, ignore_result=True)
@transaction.atomic
async def reload_localities(*, loop):
    async with get_trademe_api(loop=loop) as api:
        localities = await api.catalogue.localities()
    catalogue.Locality.objects.exclude(
        pk__in=[l.pk for l in localities]
    ).delete()
    catalogue.District.objects.filter(locality=None).delete()
    catalogue.Suburb.objects.filter(district=None).delete()
    suburbs_by_id = catalogue.Suburb.objects.all().prefetch_related(
        'adjacent_suburbs_ids'
    ).in_bulk()
    for suburb in suburbs_by_id.values():
        adj_suburbs = []
        for asid in suburb.adjacent_suburbs_ids.all():
            adj_suburbs.append(suburbs_by_id[asid.value])
        suburb.adjacent_suburbs.set(adj_suburbs)


@asyncio_task(app, ignore_result=True)
@transaction.atomic
async def reload_membership_localities(*, loop):
    async with get_trademe_api(loop=loop) as api:
        membership_localities = await api.catalogue.membership_localities()
    catalogue.MembershipLocality.objects.exclude(
        pk__in=[l.pk for l in membership_localities]
    ).delete()
    catalogue.MembershipDistrict.objects.filter(locality=None).delete()
