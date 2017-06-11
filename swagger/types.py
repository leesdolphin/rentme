
from collections.abc import Mapping
from itertools import chain


class DataDefinition(Mapping):

    def __init__(self, required=None):
        self.required = required
        self.extras = {}

    def __setitem__(self, key, value):
        if key not in self or key in self.extras:
            self.extras[key] = value

    def __iter__(self):
        if self.required is None:
            return iter(self.extras)
        else:
            return chain(self.extras, ['required'])

    def __getitem__(self, key):
        if key == 'required' and self.required is not None:
            return self.required
        if key in self.extras:
            return self.extras[key]
        raise KeyError(key)

    def __len__(self):
        return 0 if self.required is None else 1

    def __str__(self):
        return '{}({})'.format(self.__class__, super().__str__())


class RefDataDefinition(DataDefinition):

    def __init__(self, ref_name, required=None):
        self.ref_name = ref_name
        super().__init__(required=required)

    def __iter__(self):
        return chain(['$ref', 'x-ref-name'], super().__iter__())

    def __getitem__(self, key):
        if key == '$ref':
            return '#/definitions/' + self.ref_name
        elif key == 'x-ref-name':
            return self.ref_name
        else:
            return super().__getitem__(key)

    def __len__(self):
        return 2 + super().__len__()


class CollectionRefDataDefinition(DataDefinition):

    def __init__(self, ref_name, required=None):
        self.ref_name = ref_name
        super().__init__(required=required)

    def __iter__(self):
        return chain(['type', 'items'], super().__iter__())

    def __getitem__(self, key):
        if key == 'type':
            return 'array'
        elif key == 'items':
            return RefDataDefinition(self.ref_name, self.required)
        else:
            return super().__getitem__(key)

    def __len__(self):
        return 2 + super().__len__()


class PrimativeDataDefinition(DataDefinition):

    def __init__(self, data, required=None):
        self.data = data
        super().__init__(required=required)

    def __iter__(self):
        return chain(self.data, super().__iter__())

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return super().__getitem__(key)

    def __len__(self):
        return len(self.data) + super().__len__()


class CollectionPrimativeDataDefinition(DataDefinition):

    def __init__(self, item_dfn, required=None):
        self.item_dfn = item_dfn
        super().__init__(required=required)

    def __iter__(self):
        return chain(['type', 'items'], super().__iter__())

    def __getitem__(self, key):
        if key == 'type':
            return 'array'
        elif key == 'items':
            return self.item_dfn
        else:
            return super().__getitem__(key)

    def __len__(self):
        return 2 + super().__len__()
