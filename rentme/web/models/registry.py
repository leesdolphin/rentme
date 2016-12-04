import trademe.models.registry


class DjangoModelRegistry(trademe.models.registry.ModelRegistry):

    def register_django_model(self, model):
        _, _, module_name = model.__module__.rpartition('.')
        name = module_name + '.' + model.__name__
        pk_name = model._meta.pk.attname

        def fn(data):
            pk = data.pop(pk_name)
            obj, _ = model.objects.update_or_create(
                **{'defaults': data, pk_name: pk})
            return obj
        self.register(name, fn)
        return model

model_registry = DjangoModelRegistry()
