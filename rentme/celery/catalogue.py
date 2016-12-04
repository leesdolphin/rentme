import asyncio

import aiohttp
from trademe.api import RootManager

from . import app
from .utils import asyncio_task
from rentme.web.models.registry import model_registry


@app.task
@asyncio_task
async def reload_categories():
    async with aiohttp.ClientSession() as session:
        x = RootManager(session, model_registry=model_registry)
        await x.catalogue.categories()


@app.task
@asyncio_task
async def reload_localities():
    async with aiohttp.ClientSession() as session:
        x = RootManager(session, model_registry=model_registry)
        await x.catalogue.localities()


@app.task
@asyncio_task
async def reload_membership_localities():
    async with aiohttp.ClientSession() as session:
        x = RootManager(session, model_registry=model_registry)
        await x.catalogue.membership_localities()
