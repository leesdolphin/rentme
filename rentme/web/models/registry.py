import functools

from django.db.utils import IntegrityError
import trademe.models.registry


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
        pk = data.pop(pk_name)
        print("{} . {} = {} => {}".format(model, pk_name, pk, data))
        # for fk in delayed_fks:
        #     fk_ids = data.pop(fk)
        #     print("  {} => {}".format(fk, fk_ids))
        #     fk_objs = []
        #     for fk_id in fk_ids:
        #         try:
        #             fk_objs.append(model.objects.get(pk=fk_id))
        #         except model.DoesNotExist:
        #             print("  {} => {} Does not exist. Storing".format(fk, fk_id))
        #             # When the non-existant FK is created; add it to this one.
        #             self.delayed_foreign_keys.setdefault(, []).append(pk)
        #     data[fk] = fk_objs
        try:
            obj = model.objects.update_or_create(defaults=data, **{pk_name: pk})
        except IntegrityError:
            obj = model(**data, **{pk_name: pk})

        # obj = model(**data, **{pk_name: pk})
        # for fk in delayed_fks:
        #     for key in self.delayed_foreign_keys.pop((model, fk, pk), []):
        #         getattr(model.objects.get(pk=key), fk).add(obj)
        # print(self.delayed_foreign_keys)
        return obj

    def create_recording_registry(self):
        return trademe.models.registry.RecordingRegistry(self)

model_registry = DjangoModelRegistry()
