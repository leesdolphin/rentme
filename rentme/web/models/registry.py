import asyncio
import functools

from django.db.utils import IntegrityError
import trademe.models.registry
import trademe.models.search


RESOLVER_UNSUCCESSFUL_SENTINAL = object()


def asyncpartial(fn, *default_args, **default_kwargs):
    async def wrapped(*a, **k):
        kwargs = dict(default_kwargs)
        kwargs.update(k)
        return await fn(*default_args, *a, **kwargs)

    return wrapped


def default_fk_resolver(field, fk_objects, obj):
    if field.name in obj:
        item = obj[field.name]
    elif field.attname in obj:
        item = obj.pop(field.attname)
    else:
        return RESOLVER_UNSUCCESSFUL_SENTINAL
    if item is not None and not isinstance(item, field.related_model):
        return fk_objects.get(pk=item)
    return RESOLVER_UNSUCCESSFUL_SENTINAL


def listing_suburb_name_resolver(field, fk_objects, obj):
    name = obj.pop('suburb_name')
    try:
        return fk_objects.get(name=name)
    except field.related_model.MultipleObjectsReturned:
        return RESOLVER_UNSUCCESSFUL_SENTINAL


def get_attr_value_by_name(attrs, name):
    for attr in attrs:
        if attr.name == name:
            return attr.value
    return None


def listing_suburb_attribute_resolver(field, fk_objects, obj):
    suburb_name = get_attr_value_by_name(obj['attributes'], 'suburb')
    district_name = get_attr_value_by_name(obj['attributes'], 'district')
    locality_name = get_attr_value_by_name(obj['attributes'], 'locality')
    try:
        try:
            return fk_objects.get(name=suburb_name)
        except:
            try:
                return fk_objects.get(name=suburb_name,
                                      district__name=district_name)
            except:
                return fk_objects.get(name=suburb_name,
                                      district__name=district_name,
                                      district__locality__name=locality_name)
    except field.related_model.MultipleObjectsReturned:
        return RESOLVER_UNSUCCESSFUL_SENTINAL


CUSTOM_FOREIGN_KEY_RESOLVERS = {
    ('web.Listing', 'suburb'): [
        default_fk_resolver,
        listing_suburb_name_resolver,
        listing_suburb_attribute_resolver
    ]
}


class DjangoModelRegistry(trademe.models.registry.ModelRegistry):

    def __init__(self):
        super().__init__()
        self.dj_models = {}
        self.delayed_foreign_keys = {}

    def register_django_model(self, model=None, delayed_fks=None):
        def wrapped(model):
            if delayed_fks and isinstance(delayed_fks, str):
                _delayed_fks = (delayed_fks, )
            elif delayed_fks:
                _delayed_fks = tuple(delayed_fks)
            else:
                _delayed_fks = ()  # empty tuple
            _, _, module_name = model.__module__.rpartition('.')
            name = module_name + '.' + model.__name__
            self.register(name, asyncpartial(self.create_model,
                                             delayed_fks=_delayed_fks,
                                             model=model))
            self.dj_models[name] = model
            return model

        if model is None:
            return wrapped
        else:
            return wrapped(model)

    async def create_model(self, *a, **k):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, functools.partial(self.sync_create_model, *a, **k))

    def sync_create_model(self, data, *, model, delayed_fks):
        orig_data = dict(data)
        model_label = model._meta.label
        pk_name = model._meta.pk.attname
        fields = model._meta.fields
        for field in filter(lambda f: f.is_relation, fields):
            fk_objects = field.related_model.objects
            resolvers = CUSTOM_FOREIGN_KEY_RESOLVERS.get(
                (model_label, field.name), [default_fk_resolver])
            for resolver in resolvers:
                result = RESOLVER_UNSUCCESSFUL_SENTINAL
                try:
                    result = resolver(field, fk_objects, data)
                except (KeyError, field.related_model.DoesNotExist) as _:
                    pass
                if result is not RESOLVER_UNSUCCESSFUL_SENTINAL:
                    data[field.name] = result
                    break
        fk_data = dict(data)
        data = {f.name: data.get(f.name, f.get_default()) for f in fields}
        try:
            if pk_name in data:
                pk = data.pop(pk_name)
                try:
                    obj, _ = model.objects.update_or_create(defaults=data, **{pk_name: pk})
                except IntegrityError:
                    obj = model(**data, **{pk_name: pk})
                    obj.save()
            else:
                try:
                    obj, _ = model.objects.update_or_create(**data)
                except IntegrityError:
                    obj = model(**data)
                    obj.save()
                except model.MultipleObjectsReturned as e:
                    print("Multiple objects for data lookup")
                    print(data)
                    raise e
            return obj
        except:
            print("ERROR")
            print(orig_data)
            print('\n\n')
            print(fk_data)
            raise

    def create_recording_registry(self):
        return trademe.models.registry.RecordingRegistry(self)


model_registry = DjangoModelRegistry()
model_registry.register('search.SearchResults',
                        trademe.models.search.SearchResults)
