import aiohttp
from celery.utils.log import get_task_logger
from django.db import transaction

from rentme.celery import app
from rentme.celery.utils import asyncio_task, TradeMeStorer
from rentme.web.models.registry import model_registry
from trademe.api import RootManager


logger = get_task_logger(__name__)


@app.task
@asyncio_task
async def reload_categories():
    async with aiohttp.ClientSession() as session:
        x = RootManager(session)
        categories = await x.catalogue.categories()
    with transaction.atomic(), TradeMeStorer() as storer:
        storer.store_all(categories)
    return len(categories)


# @app.task
# @asyncio_task
async def reload_localities():
    async with aiohttp.ClientSession() as session:
        x = RootManager(session)
        localities = await x.catalogue.localities()
    print("Loaded localities")
    with transaction.atomic(), TradeMeStorer() as storer:
        storer.store_all(localities)
    return len(localities)


@app.task
@asyncio_task
async def reload_membership_localities():
    async with aiohttp.ClientSession() as session:
        x = RootManager(session, model_registry=model_registry)
        membership_localities = await x.catalogue.membership_localities()
    with transaction.atomic(), TradeMeStorer() as storer:
        storer.store_all(membership_localities)
    return len(membership_localities)
