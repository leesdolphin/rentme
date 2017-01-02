import asyncio
import collections
import functools

import aiohttp
from django.db import transaction
from trademe.api import RootManager
from trademe.models.base import ModelBaseClass

from . import app
from .utils import asyncio_task
from rentme.web.models.registry import model_registry


@app.task
@asyncio_task
async def reload_categories():
    async with aiohttp.ClientSession() as session:
        x = RootManager(session, model_registry=model_registry)
        with transaction.atomic():
            await x.catalogue.categories()


@app.task
@asyncio_task
async def reload_localities():
    async with aiohttp.ClientSession() as session:
        registry = model_registry.create_recording_registry()
        # registry.get_wrapped_registry(transaction.atomic)
        x = RootManager(session)
        localities = await x.catalogue.localities()
        convert_to_django(localities)
        # for model in reversed(registry.all_models):
        #     print(model)
        #     model.save()


@app.task
@asyncio_task
async def reload_membership_localities():
    async with aiohttp.ClientSession() as session:
        x = RootManager(session, model_registry=model_registry)
        with transaction.atomic():
            await x.catalogue.membership_localities()


def create_basic_model(obj):
    model, pk_name, basic_fields, _, _ = get_model_info(obj.TRADEME_API_NAME)


def store_trademe_objects_in_django(object_or_list_of_trademe_objects):
    delayed_callbacks = []


class TradeMeStorer():

    def __init__(self):
        self.delayed_callbacks = None

    def store(self, obj):
        if self.delayed_callbacks is None:
            with self:
                return self._do_store(obj)
        else:
            return self._do_store(obj)

    @staticmethod
    @functools.lru_cache(max_size=32)
    def get_model_info(trademe_name):
        model = model_registry.dj_models[trademe_name]
        pk_name = model._meta.pk.attname
        basic_field_names, one_to_many, many_to_many = [], [], []
        for field in model._meta.get_fields():
            if not field.is_relation:
                basic_field_names.append(field.attname)
            elif field.one_to_many:
                one_to_many.append(field)
            elif field.many_to_many:
                many_to_many.append(field)
        return (model, pk_name, frozenset(basic_field_names),
                frozenset(one_to_many), frozenset(many_to_many))

    def _do_store(self, obj, defaults=None):
        instance = self._upsert_base_data(obj, defaults=defaults)

    def _upsert_base_data(self, obj, defaults=None):
        assert isinstance(obj, ModelBaseClass)
        assert hasattr(obj, 'TRADEME_API_NAME'), 'Object is not a TradeMe Object'
        model, pk_name, basic_fields, _, _ = self.get_model_info(obj.TRADEME_API_NAME)
        pk = getattr(obj, pk_name)
        obj_dict = obj._asdict()
        new_obj_basics = dict(defaults or {})
        for fieldname in basic_fields:
            if fieldname in obj_dict:
                new_obj_basics[fieldname] = obj_dict.pop(fieldname)
        instance, _ = model.objects.update_or_create(defaults=new_obj_basics, **{pk_name: pk})
        return instance

    def store_all(self, objects):
        if self.delayed_callbacks is None:
            with self:
                return [self._do_store(obj) for obj in objects]
        else:
            return [self._do_store(obj) for obj in objects]

    def __enter__(self):
        assert self.delayed_callbacks is None
        self.delayed_callbacks = []

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            for cb in self.delayed_callbacks:
                cb()
        self.delayed_callbacks = None


def _convert_to_django(object_or_list_of_trademe_objects, *, delayed_callbacks, defaults=None):
    if isinstance(object_or_list_of_trademe_objects, list):
        return [
            convert_to_django(obj, defaults=defaults) for obj in object_or_list_of_trademe_objects
        ]
    obj = object_or_list_of_trademe_objects
    assert isinstance(obj, ModelBaseClass)
    assert hasattr(obj, 'TRADEME_API_NAME'), 'Object is not a TradeMe Object'
    model = model_registry.dj_models[obj.TRADEME_API_NAME]

    pk = getattr(obj, pk_name)
    obj_dict = obj._asdict()
    new_obj_basics = dict(defaults or {})
    for field in model._meta.get_fields():
        if not field.is_relation and field.attname in obj_dict:
            new_obj_basics[field.attname] = obj_dict.pop(field.attname)
    instance, _ = model.objects.update_or_create(defaults=new_obj_basics, **{pk_name: pk})
    for field in model._meta.get_fields():
        if field.one_to_many:
            our_fk_name = field.related_name
            target_name = field.remote_field.name
            old_fk_items = obj_dict.pop(our_fk_name)
            new_fk_items = []
            for item in old_fk_items:
                if isinstance(item, ModelBaseClass):
                    new_fk_items.append(convert_to_django(item, defaults={target_name: instance}))
                else:
                    new_fk_items.append(item)
            setattr(instance, our_fk_name, new_fk_items)
        if field.many_to_many:
            print(field, field.__dict__)
            our_fk_name = field.attname
            target_name = field.remote_field.name
            old_fk_items = obj_dict.pop(our_fk_name)

    instance.save()
    return instance
