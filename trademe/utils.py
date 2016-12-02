import re


def reduce_mapping(to_convert, name_mapping=None, keep_list=None):
    mapping = {}
    if name_mapping is not None:
        mapping.update(name_mapping)
    if keep_list is not None:
        mapping.update(zip(keep_list, keep_list))
    if not mapping:
        raise ValueError("No mappings supplied. Assuming this is a bug")
    assert len(mapping) == len(set(mapping.values())), "Not 1-to-1"
    new_dictionary = {}
    for key, value in to_convert.items():
        new_key = mapping.get(key, None)
        if new_key:
            new_dictionary[new_key] = value
    return new_dictionary


def title_to_snake_case_mapping(*args, extra=None, extras=None):
    name_mapping = {}
    for old_name in args:
        assert re.fullmatch(r'([A-Z]+[^A-Z ]*)+', old_name), \
               "String must be title case"
        words = re.findall(r'[A-Z]+[^A-Z]*', old_name)
        new_name = '_'.join(map(str.lower, words))
        name_mapping[old_name] = new_name
    if extra is not None:
        name_mapping.update(extra)
    if extras is not None:
        name_mapping.update(*extras)
    # Assert there is a 1-to-1 mapping between old and new names.
    assert len(name_mapping) == len(set(name_mapping.values()))
    return name_mapping
