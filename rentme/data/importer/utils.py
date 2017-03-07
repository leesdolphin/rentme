import asyncio
import collections
import functools
import time

from celery.utils.log import get_task_logger

from rentme.data.models.registry import model_registry
from trademe.models.base import ModelBaseClass


logger = get_task_logger(__name__)


KNOWN_MISSING_M2M_FKS = {
    'catalogue.Suburb': {
        # These suburbs don't exist except in the adjecency lists. :'(
        'adjacent_suburbs': frozenset([977, 1242, 1303, 2175, 3045, 3231, 3322,
                                       3391, 3528])
    }
}


def asyncio_task(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Kill the old event loop and any tasks currently running.
        old_loop = asyncio.get_event_loop()
        # while old_loop.is_running():
        #     old_loop.stop()
        #     time.sleep(0.5)
        # old_loop.close()
        new_loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(new_loop)
            return new_loop.run_until_complete(fn(*args, **kwargs))
        finally:
            asyncio.set_event_loop(old_loop)
            ex = None
            if any(map(lambda task: not task.done(),
                       asyncio.Task.all_tasks(new_loop))):
                ex = TypeError('Function did not clean up tasks.')
            new_loop.close()
            del new_loop
            if ex:
                raise ex

    return wrapper


# class AsyncTask()


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
    @functools.lru_cache(maxsize=32)
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
        assert isinstance(obj, ModelBaseClass)
        assert hasattr(obj, 'TRADEME_API_NAME'), 'Object is not a TradeMe Object'
        model_name = obj.TRADEME_API_NAME
        obj_dict = obj._asdict()
        instance = self._upsert_base_data(model_name, obj_dict, defaults=defaults)
        self._upsert_one_to_many_fks(model_name, obj_dict, instance)
        self._add_delayed_cb(self._upsert_many_to_many_fks, model_name, obj_dict, instance)

        return instance

    def _upsert_base_data(self, model_name, obj_dict, defaults=None):
        model, pk_name, basic_fields, _, _ = self.get_model_info(model_name)
        pk = obj_dict[pk_name]
        new_obj_basics = dict(defaults or {})
        for fieldname in basic_fields:
            if fieldname in obj_dict:
                new_obj_basics[fieldname] = obj_dict.pop(fieldname)
        instance, _ = model.objects.update_or_create(defaults=new_obj_basics, **{pk_name: pk})
        return instance

    def _upsert_one_to_many_fks(self, model_name, obj_dict, instance):
        _, _, _, one_to_many_fields, _ = self.get_model_info(model_name)
        for field in one_to_many_fields:
            our_fk_name = field.related_name
            target_name = field.remote_field.name
            old_fk_items = obj_dict.pop(our_fk_name, [])
            new_fk_items = []
            for item in old_fk_items:
                if isinstance(item, ModelBaseClass):
                    new_fk_items.append(self._do_store(item, defaults={target_name: instance}))
                else:
                    new_fk_items.append(item)
            setattr(instance, our_fk_name, new_fk_items)
        instance.save()

    def _upsert_many_to_many_fks(self, model_name, obj_dict, instance):
        model, pk_name, _, _, many_to_many_fields = self.get_model_info(model_name)
        for field in many_to_many_fields:
            our_fk_name = field.attname
            known_missing = KNOWN_MISSING_M2M_FKS[model_name][our_fk_name]
            old_fk_items = obj_dict.pop(our_fk_name)
            item_objs = []
            for item_id in old_fk_items:
                if item_id in known_missing:
                    continue
                try:
                    item_objs.append(model.objects.get(**{pk_name: item_id}))
                except model.DoesNotExist as e:
                    logger.warning('Cannot add %s(%s=%r). It doesn\'t exist.',
                                   model, pk_name, item_id)
            setattr(instance, our_fk_name, item_objs)
        instance.save()

    def _add_delayed_cb(self, fn, *args, **kwargs):
        self.delayed_callbacks.append(functools.partial(fn, *args, **kwargs))

    def store_all(self, objects):
        if self.delayed_callbacks is None:
            with self:
                return [self._do_store(obj) for obj in objects]
        else:
            return [self._do_store(obj) for obj in objects]

    def __enter__(self):
        assert self.delayed_callbacks is None
        self.delayed_callbacks = []
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            for cb in self.delayed_callbacks:
                cb()
        self.delayed_callbacks = None
