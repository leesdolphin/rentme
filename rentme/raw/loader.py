from __future__ import absolute_import

from datetime import date, datetime, timezone
import re

from django.db.utils import IntegrityError


class ModelDiscoverer():

    def find(self, name):
        raise KeyError('Subclasses must implement ModelDiscoverer.find')


class ModuleDiscoverer():

    def __init__(self, module):
        self.module = module

    def find(self, name):
        return getattr(self.module, name)


class MutliDiscoverer():

    def __init__(self, *discoverers):
        self.discoverers = discoverers

    def find(self, name):
        for disc in self.discoverers:
            try:
                model = disc.find(name)
                if model:
                    return model
            except (KeyError, AttributeError) as _:
                continue
        raise KeyError('Model {!r} not found'.format(name))


class ApiException(Exception):
    pass


class Deserializer():

    PRIMITIVE_TYPES = (float, bool, bytes, str, int)
    NATIVE_TYPES_MAPPING = {
        'integer': int,
        'int': int,
        'float': float,
        'number': float,
        'string': str,
        'str': str,
        'boolean': bool,
        'bool': bool,
        'date': date,
        'datetime': datetime,
        'object': object,
    }

    def __init__(self, model_discovery):
        self.model_discovery = model_discovery

    def deserialize(self, data, klass):
        '''
        Deserializes dict, list, str into an object.

        :param data: dict, list or str.
        :param klass: class literal, or string of class name.

        :return: object.
        '''
        if data is None:
            return None

        if type(klass) == str:
            if klass.startswith('list['):
                sub_kls = re.match(r'list\[(.*)\]', klass).group(1)
                return [self.deserialize(sub_data, sub_kls)
                        for sub_data in data]

            if klass.startswith('dict('):
                sub_kls = re.match(r'dict\(([^,]*), (.*)\)', klass).group(2)
                return {k: self.deserialize(v, sub_kls)
                        for k, v in data.items()}

            # convert str to class
            if klass in self.NATIVE_TYPES_MAPPING:
                klass = self.NATIVE_TYPES_MAPPING[klass]
            else:
                klass = self.model_discovery.find(klass)
                assert klass

        if klass in self.PRIMITIVE_TYPES:
            return self.deserialize_primitive(data, klass)
        elif klass == object:
            return self.deserialize_object(data)
        elif klass == date:
            return self.deserialize_date(data)
        elif klass == datetime:
            return self.deserialize_datatime(data)
        else:
            return self.deserialize_model(data, klass)

    def deserialize_primitive(self, data, klass):
        '''
        Deserializes string to primitive type.

        :param data: str.
        :param klass: class literal.

        :return: int, long, float, str, bool.
        '''
        try:
            return klass(data)
        except TypeError:
            return data

    def deserialize_object(self, value):
        '''
        Return a original value.

        :return: object.
        '''
        return value

    def deserialize_datatime(self, string):
        '''
        Deserializes string to datetime.

        The string should be in iso8601 datetime format.

        :param string: str.
        :return: datetime.
        '''
        try:
            tm_date = self.deserialize_tm_datetime(string)
            if tm_date:
                return tm_date
            from dateutil.parser import parse
            return parse(string)
        except ImportError:
            return string
        except ValueError:
            raise ApiException(
                status=0,
                reason=(
                    'Failed to parse `{0}` into a datetime object'
                    .format(string)
                )
            )

    def deserialize_tm_datetime(self, string):
        if not string:
            return None
        match = re.fullmatch(r'/Date\(([1-9][0-9]*|0)\)/', string)
        if match:
            utc_unix_seconds = int(match.group(1)) / 1000
            return datetime.fromtimestamp(utc_unix_seconds,
                                          tz=timezone.utc)
        else:
            return None

    def deserialize_model(self, data, klass):
        '''
        Deserializes list or dict to model.

        :param data: dict, list.
        :param klass: class literal.
        :return: model object.
        '''
        instance = klass()

        if not instance.swagger_types:
            return data

        if not isinstance(data, (dict, )):
            if hasattr(instance, 'expect_single_value'):
                key = instance.expect_single_value
                value = self.deserialize(data, instance.swagger_types[key])
                setattr(instance, key, value)
                try:
                    instance.save()
                except IntegrityError:
                    instance = klass.objects.get(**{key: value})
                    setattr(instance, key, value)
                    instance.save()
                return instance

        if data is None or not isinstance(data, (dict, )):
            return instance

        m2m = {}
        attrs = {}

        for attr, attr_type in instance.swagger_types.items():
            key = next(
                (key for key in instance.attribute_map.getall(attr, [])
                 if key in data),
                None)
            if key is not None:
                value = data[key]
                if attr_type.startswith('list['):
                    m2m[attr] = self.deserialize(value, attr_type)
                else:
                    attrs[attr] = self.deserialize(value, attr_type)
        try:
            for name, value in attrs.items():
                setattr(instance, name, value)
            instance.save()
        except IntegrityError:
            instance = klass.objects.get(**attrs)
            for name, value in attrs.items():
                setattr(instance, name, value)
            instance.save()

        for attr, val in m2m.items():
            getattr(instance, attr).set(val)

        return instance
