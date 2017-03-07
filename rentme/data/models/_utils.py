from collections import OrderedDict

from django.db import models


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
        del kwargs["choices"]
        kwargs['enum'] = self.enum_class
        return name, path, args, kwargs
