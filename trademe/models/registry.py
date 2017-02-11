import collections
from types import MappingProxyType

from trademe.models.base import ModelBaseClass
from trademe.utils import function_to_async_coro


ModelRegistryEntry = collections.namedtuple('ModelRegistryEntry',
                                            'fn, use_kwargs')


class ImmutableModelRegistry():

    def get_model(self, name):
        raise NotImplemented

    def create_recording_registry(self):
        return RecordingRegistry(self)


class ModelRegistry(ImmutableModelRegistry):

    def __init__(self):
        self.models = {}
        self.model_instances = {}

    def register(self, name, fn_or_class=None, *,
                 overwrite=False, use_kwargs=False):
        def wrapper(fn_or_class):
            if not overwrite:
                assert name not in self.models, ('Cannot overwrite model %r '
                                                 'as it has already been '
                                                 'registered' % (name, ))
            self.models[name] = ModelRegistryEntry(
                function_to_async_coro(fn_or_class), use_kwargs)
            return fn_or_class
        if fn_or_class:
            return wrapper(fn_or_class)
        else:
            return wrapper

    def register_namedtuple_model(self, name, required=(),
                                  defaults=(), lists=(), dicts=(), enums=()):
        attrs = set()
        required = frozenset(required)
        defaults = MappingProxyType(dict(defaults))
        lists = frozenset(lists)
        dicts = frozenset(dicts)
        enums = MappingProxyType(dict(enums))
        attrs = attrs.union(required, defaults.keys(), lists, dicts)
        assert attrs, 'At least 1 attribute must be specified.'

        cls_name = name.replace('.', '_')
        base = collections.namedtuple(cls_name + 'Base', sorted(attrs))

        def class__new(cls, __data, **data):
            if __data:
                assert not data
                data = __data
            assert required.issubset(data), \
                'Missing some required arguments for %s - %r' % (name, required.difference(data))
            assert attrs.issuperset(data), \
                'Some arguments unsupported for %s - %r' % (name, set(data).difference(attrs))
            out_data = defaults.copy()
            out_data.update(data)
            for list_name in lists:
                if list_name in out_data and out_data[list_name] is not None:
                    out_data[list_name] = tuple(out_data[list_name])
            for dict_name in dicts:
                if dict_name in out_data and out_data[dict_name] is not None:
                    out_data[dict_name] = \
                        MappingProxyType(dict(out_data[dict_name]))
            for enum_name, enum_type in enums.items():
                if enum_name in out_data and out_data[enum_name] is not None:
                    val = out_data[enum_name]
                    if not isinstance(val, enum_type):
                        if val in enum_type.__members__:
                            val = enum_type.__members__[val]
                        else:
                            val = enum_type(val)
                    out_data[enum_name] = val
            try:
                return base.__new__(cls, **out_data)
            except TypeError as e:
                raise TypeError('Cannot create model {}'.format(name)) from e

        cls = type(cls_name, (base, ModelBaseClass, object),
                   dict(__new__=class__new, __slots__=(),
                        TRADEME_API_NAME=name))
        self.register(name, cls)
        return cls

    def get_model(self, name):
        model_fn, use_kwargs = self.models[name]
        if use_kwargs:
            async def wrapper(data):
                try:
                    return await model_fn(**data)
                except Exception as e:
                    raise Exception('Creating model for {} failed.'.format(name)) from e
            return wrapper
        return model_fn


class RecordingRegistry(ImmutableModelRegistry):

    def __init__(self, parent_registry):
        self.parent = parent_registry
        self.all_models = []
        self.models_by_name = {}

    def get_model(self, name):
        model_fn = self.parent.get_model(name)

        def registration_wrapper(*args, **kwargs):
            model = model_fn(*args, **kwargs)
            self.all_models.append(model)
            self.models_by_name.setdefault(name, []).append(model)
            return model
        return registration_wrapper


model_registry = ModelRegistry()
