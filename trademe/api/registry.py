import collections
import functools
import re
import types

from trademe.models.registry import model_registry as default_model_registry
from trademe.utils import function_to_async_coro


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


class ParserRegistryBase():

    def __init__(self):
        self.parsers = {}
        self._model_registry = default_model_registry

    def get_proxy(self, model_registry=None, parser_registry=None):
        model_reg = model_registry or self._model_registry
        parser_reg = parser_registry or self

        return PreconfigiguredParserRegistryProxy(parser_reg, model_reg)

    def get_wrapped_registry(self, wrapper_fn, parser_registry=None):
        return WrappingParserRegistryProxy(parser_registry or self, wrapper_fn)

    @property
    def model_registry(self):
        return self._model_registry


class ParserRegistry(ParserRegistryBase):

    def register(self, name, overwrite=False, auto_model=False):
        def wrapper(fn):
            if not overwrite:
                assert name not in self.parsers
            self.parsers[name] = ParserRegistryEntry(
                function_to_async_coro(fn), auto_model)
            return fn
        return wrapper

    def get_parser(self, name, **kwargs):
        return self.wrap_parser(name, **kwargs)

    def wrap_parser(self, parser_name,
                    model_registry=None, parser_registry=None):
        parser_fn, parser_auto_model = self.parsers[parser_name]
        model_reg = model_registry or self._model_registry
        parser_reg = self.get_proxy(model_reg, parser_registry)

        @functools.wraps(parser_fn)
        async def wrapped(json_response, *args,
                          model_registry=None, parser_registry=None, **kwargs):
            model_registry = model_registry or model_reg
            parser_registry = parser_registry or parser_reg
            kwargs['parser_registry'] = parser_registry
            if not parser_auto_model:
                kwargs['model_registry'] = model_registry
                return await parser_fn(json_response, *args, **kwargs)
            else:
                model_init_kwargs = await parser_fn(json_response, *args, **kwargs)
                dates = []
                caps_keys = []
                for k, v in model_init_kwargs.items():
                    if str(v).startswith('/Date('):
                        dates.append(k)
                    if re.search('[A-Z]', k):
                        caps_keys.append(k)
                try:
                    model_fn = model_registry.get_model(parser_name)
                except KeyError as e:
                    raise KeyError('Cannot find model function. '
                                   'Given data: {}'.format(model_init_kwargs)) from e
                return await model_fn(model_init_kwargs)
        return wrapped


parser_registry = ParserRegistry()


class WrappingParserRegistryProxy(ParserRegistry):

    def __init__(self, parser_registry, wrapper_fn):
        super().__init__()
        self.parsers = types.MappingProxyType(parser_registry.parsers)
        self._wrapper_fn = wrapper_fn

    def wrap_parser(self, *args, **kwargs):
        return self._wrapper_fn(self._parser_registry.wrap_parser(*args, **kwargs))


class PreconfigiguredParserRegistryProxy(ParserRegistry):

    def __init__(self, parser_registry, model_registry):
        super().__init__()
        self.parsers = types.MappingProxyType(parser_registry.parsers)
        self._parser_registry = parser_registry
        self._model_registry = model_registry or default_model_registry

    def register(self, *a, **k):
        raise ValueError('Cannot register a parser on a proxy object')
