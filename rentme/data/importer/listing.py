import aiohttp
from celery.utils.log import get_task_logger
from django.db import transaction

from rentme.data.importer.celery import app
from rentme.data.importer.utils import asyncio_task, TradeMeStorer
from rentme.data.models.registry import model_registry
from trademe.api import RootManager


logger = get_task_logger(__name__)


@app.task
@asyncio_task
async def reload_listing(listing_id):
    async with aiohttp.ClientSession() as session:
        x = RootManager(session, model_registry=model_registry)
        listing = await x.listing.listing(listing_id)
    print(listing)
    with transaction.atomic(), TradeMeStorer() as storer:
        storer.store(listing)
