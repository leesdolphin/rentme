from math import ceil

from django.db import models


class BinaryStringField(models.CharField):

    def __init__(self, *a, bit_length=None, byte_length=None, **kwargs):
        if 'max_length' in kwargs:
            raise ValueError('Cannot specify max_length. Use bit_length or byte_length')
        if bit_length is None and byte_length is None:
            raise ValueError('Must specify one of bit_length or byte_length')
        elif byte_length is not None:
            bit_length = byte_length * 8
        self.bit_length = bit_length
        super().__init__(self, *a, max_length=ceil(bit_length / 6))

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop('max_length', None)
        kwargs['byte_length'] = self.byte_length
        return name, path, args, kwargs

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        return numpyarray

    def value_to_string(self, obj):
        return b64encode(obj if obj is a numpyarray)

    def get_prep_value(self, obj):
        return b64encode(obj if obj is a numpyarray)


class ImageHashInformation():

    url = models.URLField()
    sha512 = models.BinaryStringField()
    p_hash = models.BinaryStringField()
    w_hash = models.BinaryStringField()
