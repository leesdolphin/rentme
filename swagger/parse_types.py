
from . import types


def load_enum_into_item(enum_row, data):
    t, _, values, _ = enum_row
    assert t == 'enum'
    _, has_value, _ = values[0]
    if has_value is None:
        data['enum'] = [k for k, _, _ in values]
        data['type'] = 'string'
        data['x-named-enum'] = [
            {
                'key': k,
                'value': k,
                'description': desc,
            }
            for k, _, desc in values
        ]
    else:
        data['enum'] = [v for _, v, _ in values]
        data['type'] = 'integer'
        data['format'] = 'int64'
        data['x-keyed-enum'] = [
            {
                'key': k,
                'value': v,
                'description': desc,
            }
            for k, v, desc in values
        ]
    return data


def parse_type_format(value):
    if value[0] == '<':
        ref, _, extra = value[1:].partition('>')
        if '`' in ref:
            ref, _, _ = ref.partition('`')
        data_dfn = types.RefDataDefinition(ref)
        if not extra:
            return data_dfn
    elif value.startswith('Collection of '):
        data_dfn = parse_type_format(value[len('Collection of '):])
        if isinstance(data_dfn, types.PrimativeDataDefinition):
            return types.CollectionPrimativeDataDefinition(
                data_dfn, data_dfn.required)
        else:
            return types.CollectionRefDataDefinition(
                data_dfn.ref_name, data_dfn.required)
    else:
        swagger_types = {
            'Integer': ('integer', 'int64'),
            'String': ('string', ''),
            'Number': ('number', 'double'),
            'DateTime': ('string', 'date-time'),
            'Boolean': ('boolean', ''),
        }
        if value.startswith('Long Integer'):
            v_type = 'Integer'
            extra = value[len('Long Integer'):]
        else:
            v_type, _, extra = value.partition(' ')
        if v_type == 'Enumeration':
            data = {
                'enum': True,
            }
        elif v_type == 'DateTime':
            data = {
                'type': 'string',
                'format': 'date-time',
                'x-tm-datetime': True,
            }
        elif v_type in swagger_types:
            t, f = swagger_types[v_type]
            data = {'type': t}
            if f:
                data['format'] = f
        else:
            print(value, repr(v_type))
            raise Exception('ssss')
        data_dfn = types.PrimativeDataDefinition(data)
        del data
    extra = extra.strip() if extra else ''
    # if extra == '(optional)':
    #     data_dfn.required = False
    # elif extra == '(required)':
    #     data_dfn.required = True
    return data_dfn
