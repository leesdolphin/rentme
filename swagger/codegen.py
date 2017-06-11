import keyword
import string
from textwrap import wrap

import inflection


DJANGO_MODELS = {
    'string': {
        None: ('str', 'models.TextField'),
        'date-time': ('datetime', 'models.DateTimeField'),
    },
    'boolean': {
        None: ('bool', 'models.NullBooleanField'),
    },
    'integer': {
        'int64': ('int', 'models.IntegerField'),
    },
    'number': {
        'double': ('float', 'models.FloatField'),
    },
}


def to_python_name(camel_name):
    pyname = inflection.underscore(camel_name)
    if keyword.iskeyword(pyname):
        pyname = pyname + '_'
    return pyname


CHARS = frozenset(string.ascii_letters + string.digits)


def to_multiline_string(str, indent=0, max_len=80):
    reprstr = repr(str)
    quote_char = reprstr[0]
    wrap_len = max_len - indent - 2
    wrapped = wrap(reprstr[1:-1], wrap_len, drop_whitespace=False)
    sep = quote_char + '\n' + (' ' * indent) + quote_char
    return quote_char + sep.join(wrapped) + quote_char


def enum_to_choices(choices):
    c = '(\n' + (' ' * 12)
    items = []
    for item in choices:
        if len(item) == 2:
            items.append(
                '({key!r}, {value!r})'.format(key=item[0], value=item[1])
            )
        elif len(item) == 1:
            items.append(
                '({key!r}, {value!r})'.format(key=item[0], value=item[0])
            )

    c += (',\n' + (' ' * 12)).join(items)
    return c + ',\n' + (' ' * 8) + ')'


def quote(string):
    return repr(string)


def generate_models_for_definition(name, dfn, *, model_args={}):
    if name in ['ListingRequest', 'DraftListing']:
        return []
    model = {
        'classname': name,
        'baseclass': 'models.Model',
        'attr_map': [],
        'extra_model_attrs': model_args
    }
    model_pyname = to_python_name(name)
    fields = []
    other_models = []
    lower_keys = {key.lower(): key for key in dfn.keys()}
    uniqueness = []
    for possible_pk in ['id', (name + 'id')]:
        if possible_pk.lower() in lower_keys:
            uniqueness.append([
                to_python_name(lower_keys[possible_pk.lower()])
            ])
    print(name)
    if name in ['ListedItemDetail', 'Flatmate']:
        uniqueness = [['listing_id']]
    if name in ['PhotoUrl']:
        uniqueness = [['photo_id']]
    if name in ['Photo']:
        model['attr_map'].append(('photo_id', 'Key'))
    if uniqueness:
        model['uniqueness'] = uniqueness
    for vname, attr in sorted(dfn.items()):
        attr = dict(attr)
        pyname = to_python_name(vname)
        field = {
            'attribute': pyname,
            'key': vname,
            'kwargs': {'null': True},
        }
        model['attr_map'].append((pyname, vname))
        if '$ref' in attr:
            if 'x-ref-name' in attr:
                attr.pop('$ref')
                ref_name = attr.pop('x-ref-name')
            else:
                _, _, ref_name = attr.pop('$ref').rpartition('/')
            field['swagger_type'] = ref_name
            field['django_type'] = 'models.ForeignKey'
            field['args'] = (quote(ref_name), )
            field['kwargs'] = {
                'related_name': quote(model_pyname + '_reverse_' + pyname),
                'on_delete': 'models.CASCADE',
                'null': 'True',
                'blank': 'True'
            }
        elif attr.get('type') == 'array':
            attr.pop('type')
            items = attr.pop('items')
            if items.get('type') in DJANGO_MODELS:
                # Generate a specical model to hold this list.
                ref_name = name + vname
                other_models += generate_models_for_definition(ref_name, {
                    'value': items,
                }, model_args={'expect_single_value': quote('value')})
            elif items.get('$ref'):
                if 'x-ref-name' in items:
                    ref_name = items.get('x-ref-name')
                else:
                    _, _, ref_name = items.get('$ref').rpartition('/')
            else:
                print(attr, items)
                raise Exception("SDFSDF")
            field['swagger_type'] = 'list[' + ref_name + ']'
            field['django_type'] = 'models.ManyToManyField'
            field['args'] = (quote(ref_name), )
            field['kwargs'] = {
                'related_name': quote(model_pyname + '_reverse_' + pyname),
            }
        elif not attr.get('type'):
            print("Invalid type", name, vname, attr)
            print(dfn[vname])
            raise Exception()
        elif attr['type'] in DJANGO_MODELS:
            t = attr.pop('type')
            f = attr.pop('format', None)
            if f == 'date-time':
                attr.pop('x-tm-datetime')
            field['swagger_type'], field['django_type'] = DJANGO_MODELS[t][f]
        if 'description' in attr:
            field['kwargs']['help_text'] = to_multiline_string(
                attr.pop('description'), indent=18, max_len=78)
        if 'required' in attr:
            field['kwargs']['blank'] = not attr.pop('required')
        if 'x-named-enum' in attr or 'x-keyed-enum' in attr:
            attr.pop('enum')
            if 'x-keyed-enum' in attr:
                enums = attr.pop('x-keyed-enum')
            else:
                enums = attr.pop('x-named-enum')
            valCast = str
            if field['django_type'] == 'models.IntegerField':
                valCast = int
            field['kwargs']['choices'] = enum_to_choices(
                (valCast(d['value']), d['key']) for d in enums)
        if 'enum' in attr:
            valCast = str
            if field['django_type'] == 'models.IntegerField':
                valCast = int
            field['kwargs']['choices'] = enum_to_choices(
                (valCast(key), key) for key in attr.pop('enum'))
        if attr or not field['django_type']:
            print("Invalid type", name, vname, attr)
            print(dfn[vname])
            raise Exception()
        if [field['attribute']] in uniqueness:
            field['kwargs']['primary_key'] = True
            del field['kwargs']['null']
        fields.append(field)
    if 'uniqueness' not in model:
        non_m2m_fields = [field['attribute']
                          for field in fields
                          if 'ManyToMany' not in field['django_type']]
        if non_m2m_fields:
            model['uniqueness'] = [non_m2m_fields]
    if any(len(uniq) >= 32 for uniq in model.get('uniqueness', [])):
        raise Exception("Uniqueness not valid for model {!r}".format(name))
    model['fields'] = fields
    return other_models + [model]


def generate_django_for_definitions(definitions):
    template_ctx = {
        'imports': [
            'from django.db import models',
        ]
    }

    from jinja2 import Template
    with open('/home/lee/Scratchpad/rentme/swagger/templates/model.py.j2') \
            as f:
        template = Template(
            f.read(),
            autoescape=False,
        )

    models = []
    for name, dfn in sorted(definitions.items()):
        models += generate_models_for_definition(name, dfn['properties'])

    code = template.render(models=models, **template_ctx)
    with open('tm_models.py', 'w') as f:
        f.write(code)


if __name__ == '__main__':
    import json
    with open('swagger.json') as f:
        swagger = json.load(f)

    dfns = swagger['definitions']

    generate_django_for_definitions(swagger['definitions'])
