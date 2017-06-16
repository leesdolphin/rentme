from celery.utils.log import get_task_logger
from django.db import transaction
from django.db.models import Q

from rentme.raw.importer.celery import app
from aioutils.celery import asyncio_task
from rentme.raw.api import get_trademe_api
from rentme.data.models import catalogue


logger = get_task_logger(__name__)


@asyncio_task(app)
async def reload_categories(*, loop):
    async with get_trademe_api(loop=loop) as api:
        categories = await api.catalogue.categories()
    print(categories)
    # for category in catalogue.Category.objects.filter(id__not_in=categories):
    #


@asyncio_task(app, ignore_result=True)
async def reload_localities(*, loop):
    async with get_trademe_api(loop=loop) as api:
        localities = await api.catalogue.localities()


@asyncio_task(app)
async def reload_membership_localities(*, loop):
    async with get_trademe_api(loop=loop) as api:
        membership_localities = await api.catalogue.membership_localities()

    return len(membership_localities)
