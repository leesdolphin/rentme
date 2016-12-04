import collections
from types import MappingProxyType

ModelRegistryEntry = collections.namedtuple('ModelRegistryEntry',
                                            'fn, use_kwargs')


class ModelRegistry():

    def __init__(self):
        self.models = {}
        self.model_instances = {}

    def register(self, name, fn_or_class=None, *,
                 overwrite=False, use_kwargs=False):
        def wrapper(fn_or_class):
            if not overwrite:
                assert name not in self.models
            self.models[name] = ModelRegistryEntry(fn_or_class, use_kwargs)
            return fn_or_class
        if fn_or_class:
            return wrapper(fn_or_class)
        else:
            return wrapper

    def register_namedtuple_model(self, name, required=(),
                                  defaults=(), lists=(), dicts=()):
        attrs = set()
        required = frozenset(required)
        defaults = MappingProxyType(dict(defaults))
        lists = frozenset(lists)
        dicts = frozenset(dicts)
        attrs = attrs.union(required, defaults.keys(), lists, dicts)
        assert attrs, "At least 1 attribute must be specified."

        cls_name = name.replace('.', '_')
        base = collections.namedtuple(cls_name + 'Base', sorted(attrs))

        def class__new(cls, __data, **data):
            if __data:
                assert not data
                data = __data
            assert False
            assert required.issubset(data), "Missing some required arguments"
            out_data = defaults.copy()
            out_data.update(data)
            for list_name in lists:
                if list_name in out_data and out_data[list_name] is not None:
                    out_data[list_name] = tuple(data[list_name])
            for dict_name in dicts:
                if dict_name in out_data and out_data[dict_name] is not None:
                    out_data[dict_name] = \
                        MappingProxyType(dict(data[dict_name]))
            return base.__new__(cls, **out_data)

        cls = type(cls_name, (base, object),
                   dict(__new__=class__new, __slots__=()))
        self.register(name, cls)
        return cls
        #

    def get_model(self, name):
        model_fn, use_kwargs = self.models[name]
        if use_kwargs:
            return lambda data: model_fn(**data)
        return model_fn


model_registry = ModelRegistry()
