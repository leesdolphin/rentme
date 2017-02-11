import asyncio
import datetime
import functools
import inspect
import re

from trademe.async_utils import KeyedMutliAsyncBlock


def function_to_async_coro(fn):
    print(fn, inspect.iscoroutinefunction(fn))
    if not inspect.iscoroutinefunction(fn):
        old_fn = fn

        @functools.wraps(fn)
        async def fn(*a, **k):
            return old_fn(*a, **k)
    return fn


def reduce_mapping(to_convert, name_mapping=None, keep_list=None, ignore_keys=None):
    mapping = {}
    if name_mapping is not None:
        mapping.update(name_mapping)
    if keep_list is not None:
        mapping.update(zip(keep_list, keep_list))
    if not mapping:
        raise ValueError('No mappings supplied. Assuming this is a bug')
    assert len(mapping) == len(set(mapping.values())), 'Not 1-to-1'
    if ignore_keys is not None:
        mapping.update(dict.fromkeys(ignore_keys, False))
    new_dictionary = {}
    skipped_keys = []
    for key, value in to_convert.items():
        new_key = mapping.get(key, None)
        if new_key:
            new_dictionary[new_key] = value
        elif new_key is None:
            skipped_keys.append(key)
    if skipped_keys:
        raise ValueError('Reduce Mapping skipped the following keys %r' % (skipped_keys,))
    return new_dictionary


def title_to_snake_case_mapping(*args, extra=None, extras=None, prefix=''):
    name_mapping = {}
    for old_name in args:
        assert re.fullmatch(r'([A-Z]+[^A-Z ]*)+', old_name), \
               'String must be title case'
        words = re.findall(r'[A-Z]+[^A-Z]*', old_name)
        new_name = '_'.join(map(str.lower, words))
        name_mapping[old_name] = prefix + new_name
    if extra is not None:
        name_mapping.update(extra)
    if extras is not None:
        name_mapping.update(*extras)
    # Assert there is a 1-to-1 mapping between old and new names.
    assert len(name_mapping) == len(set(name_mapping.values()))
    return name_mapping


def convert_tm_date_to_datetime(date_string):
    if not date_string:
        return None
    match = re.fullmatch(r'/Date\(([1-9][0-9]*|0)\)/', date_string)
    if match:
        utc_unix_seconds = int(match.group(1)) / 1000
        return datetime.datetime.fromtimestamp(utc_unix_seconds,
                                               tz=datetime.timezone.utc)
    else:
        raise ValueError('The given date string(%r) is not in a supported'
                         ' format' % (date_string, ))


def date_convert(obj, *keys_to_convert):
    for key in keys_to_convert:
        if key in obj:
            obj[key] = convert_tm_date_to_datetime(obj[key])
    return obj


def enum_convert(obj, keys_to_enum_mapping):
    for key, enum_cls in dict(keys_to_enum_mapping).items():
        if key in obj:
            try:
                obj[key] = enum_cls(obj[key])
            except:
                obj[key] = enum_cls.__members__[obj[key]]
    return obj


async def parser_convert_singles(obj, parser_registry, conversion_dict):
    ab = KeyedMutliAsyncBlock()
    for key, parser_name in conversion_dict.items():
        if key in obj:
            parser = parser_registry.get_parser(parser_name)
            ab.add(key, parser(obj[key]))
    async for key, returned_obj in ab:
        obj[key] = returned_obj
    return obj


async def parser_convert_lists(obj, parser_registry, conversion_dict):
    ab = KeyedMutliAsyncBlock()
    for key, parser_name in conversion_dict.items():
        if key in obj:
            parser = parser_registry.get_parser(parser_name)
            items = []
            for item in obj[key]:
                items.append(parser(item))
            ab.add(key, asyncio.gather(*items))
    async for key, returned_obj in ab:
        obj[key] = list(returned_obj)
    return obj
