from collections import OrderedDict

from django.db import models
from django.core.exceptions import FieldDoesNotExist

def get_enum_choices(cls):
    if hasattr(cls, 'choices') and callable(getattr(cls, 'choices')):
        return cls.choices()
    labels = OrderedDict((member.value, name)
                         for name, member in cls.__members__.items())
    default_labels = getattr(cls, 'labels', getattr(cls, '__labels__', {}))
    for enum_value, updated_label in default_labels.items():
        labels[enum_value] = updated_label
    # In Enum order here; swap the order again so that name maps to enum.
    return tuple((name, enum_value)
                 for enum_value, name in labels.items())


class EnumIntegerField(models.IntegerField):

    def __init__(self, enum, *args, **kwargs):
        assert 'choices' not in kwargs
        choices = get_enum_choices(enum)
        super().__init__(*args, **kwargs, choices=choices)
        self.enum_class = enum

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, self.enum_class):
            return value
        else:
            # Pass validation off to the enum.Enum constructor.
            return self.enum_class(value)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return self.enum_class(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        elif isinstance(value, self.enum_class):
            # Enum's value
            return value.value
        else:
            return value

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['choices']
        kwargs['enum'] = self.enum_class
        return name, path, args, kwargs


def _fields_to_format(fields):
    return ', '.join(f + '={o.' + f + '!r}' for f in fields)


def default_debug_methods(_cls=None, *, str_fields=None):
    def wrapper(cls):
        def dstr(obj):
            nonlocal str_fields
            cn = cls.__name__
            meta = cls._meta
            if str_fields is None:
                str_fields = []
                if not meta.pk.auto_created:
                    str_fields.append(meta.pk.name)
                for check_field in ['name', 'title', 'full_name', 'nickname', 'path']:
                    try:
                        meta.get_field(check_field)
                        str_fields.append(check_field)
                    except FieldDoesNotExist:
                        pass
            str_format = cn + '(' + _fields_to_format(str_fields) + ')'
            cls.__str__ = lambda o: str_format.format(o=o)
            return str(obj)

        def drepr(obj):
            cn = cls.__name__
            meta = cls._meta
            repr_fields = [
                f.name
                for f in meta.get_fields()
                if not f.auto_created and (
                    not f.is_relation or f.one_to_one or f.many_to_one
                )
            ]
            repr_format = cn + '(' + _fields_to_format(repr_fields) + ')'
            cls.__repr__ = lambda o: repr_format.format(o=o)
            return repr(obj)

        cls.__str__ = dstr
        cls.__repr__ = drepr
        return cls

    if _cls:
        return wrapper(_cls)
    else:
        return wrapper
