import functools

from django.db.utils import IntegrityError
import trademe.models.registry
import trademe.models.search


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
            self.register(name, functools.partial(self.create_model,
                                                  delayed_fks=_delayed_fks,
                                                  model=model))
            self.dj_models[name] = model
            return model

        if model is None:
            return wrapped
        else:
            return wrapped(model)

    def create_model(self, data, *, model, delayed_fks):
        pk_name = model._meta.pk.attname
        fields = model._meta.fields
        for field in filter(lambda f: f.is_relation, fields):
            if field.name in data:
                item = data[field.name]
            elif field.attname in data:
                item = data.pop(field.attname)
            else:
                continue
            if item is not None and not isinstance(item, field.related_model):
                try:
                    data[field.name] = field.related_model.objects.get(pk=item)
                except field.related_model.DoesNotExist:
                    continue

        if pk_name in data:
            pk = data.pop(pk_name)
            # print("{} . {} = {} => {}".format(model, pk_name, pk, data))
            try:
                obj, _ = model.objects.update_or_create(defaults=data, **{pk_name: pk})
            except IntegrityError:
                obj = model(**data, **{pk_name: pk})
        else:
            try:
                obj, _ = model.objects.update_or_create(**data)
            except IntegrityError:
                obj = model(**data)
        return obj

    def create_recording_registry(self):
        return trademe.models.registry.RecordingRegistry(self)

model_registry = DjangoModelRegistry()
model_registry.register('search.SearchResults', trademe.models.search.SearchResults)
