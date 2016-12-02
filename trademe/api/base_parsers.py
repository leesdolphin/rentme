import collections
import functools
import types


def simple_rename_parser(renaming_dict):
    def wrapper(fn):
        @functools.wraps(fn)
        def wrapped(json_response, *args, **kwargs):
            update_dict = dict(json_response)
            for old_name, new_name in renaming_dict:
                if old_name in update_dict:
                    update_dict[new_name] = update_dict.pop(old_name)
            return fn(json_response, *args, **kwargs)
        return wrapped
    return wrapper


ParserRegistryEntry = collections.namedtuple('ParserRegistryEntry',
                                             'fn, auto_model')


class ParserRegistry():

    def __init__(self):
        from trademe.models import model_registry as default_model_registry
        self.parsers = {}
        self._model_registry = default_model_registry

    def register(self, name, overwrite=False, auto_model=False):
        def wrapper(fn):
            if not overwrite:
                assert name not in self.parsers
            self.parsers[name] = ParserRegistryEntry(fn, auto_model)
            return fn
        return wrapper

    def get_proxy(self, model_registry=None, parser_registry=None):
        model_reg = model_registry or self._model_registry
        parser_reg = parser_registry or self

        return PreconfigiguredParserRegistryProxy(parser_reg, model_reg)

    def get_parser(self, name, **kwargs):
        return self.wrap_parser(name, **kwargs)

    def wrap_parser(self, parser_name,
                    model_registry=None, parser_registry=None):
        parser_fn, parser_auto_model = self.parsers[parser_name]
        model_reg = model_registry or self._model_registry
        parser_reg = parser_registry or self

        @functools.wraps(parser_fn)
        def wrapped(json_response, *args,
                    model_registry=None, parser_registry=None, **kwargs):
            model_registry = model_registry or model_reg
            parser_registry = parser_registry or parser_reg
            kwargs['parser_registry'] = parser_registry
            if not parser_auto_model:
                kwargs['model_registry'] = model_registry
                return parser_fn(json_response, *args, **kwargs)
            else:
                model_init_kwargs = parser_fn(json_response, *args, **kwargs)
                return model_registry.get_model(parser_name)(model_init_kwargs)
        return wrapped


parser_registry = ParserRegistry()


class PreconfigiguredParserRegistryProxy(ParserRegistry):

    def __init__(self, parser_registry, model_registry):
        while hasattr(parser_registry, '_parser_registry'):
            # Recurse up any proxy tree we have to get to the 'root' registry.
            parser_registry = parser_registry._parser_registry
        self.parsers = types.MappingProxyType(parser_registry.parsers)
        self._parser_registry = parser_registry
        self._model_registry = model_registry

    def register(self, *a, **k):
        raise ValueError("Cannot register a parser on a proxy object")
