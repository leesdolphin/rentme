import datetime
import functools
import math


ValidationErrors = (ValueError, )


def validate_int(param):
    return str(int(param))


def validate_bool(param):
    return 'true' if bool(param) else 'false'


def validate_str(param):
    return str(param)


def validate_float(param):
    f = float(param)
    if not math.isfinite(f):
        raise ValueError('Parameter {!r} must produce a finite float. Got {!r}'
                         .format(param, f))
    return f


def validate_datetime(param):
    if not isinstance(param, datetime.datetime):
        raise ValueError('Parameter {!r} must be a datetime instance.'
                         .format(param))
    return '/Date(%d)/' % (int(param.timestamp() * 1000), )


def build_list_validator(subvalidator, *, str_sep=',', empty=True):
    def validate_list(param):
        if isinstance(param, str):
            if ',' in param:
                param_list = param.split(',')
            elif param:
                param_list = [param]
            else:
                param_list = []
        else:
            param_list = param
        if not empty and not param_list:
            raise ValueError('Empty list given and not allowed. {!r}'
                             .format(param))
        new_list = []
        for idx, item in enumerate(param_list):
            try:
                new_item = subvalidator(item)
            except ValidationErrors as e:
                raise ValueError('Parameter at index {} failed '
                                 'validation with message {!r}'
                                 .format(idx, str(e)))
            new_list.append(str(new_item))
        return str_sep.join(new_list)
    return validate_list


def build_enum_validator(enum_cls):
    return lambda param: enum_cls(param).name


class ParameterValidator():

    @classmethod
    def decorator(cls, **kwargs):
        def inner(fn):
            validator = cls(**kwargs)

            @functools.wraps(fn)
            def func(*args, **kwargs):
                cleaned_kwargs = validator(**kwargs)
                return fn(*args, **cleaned_kwargs)

            return func
        return inner

    def __init__(
        self,
        _integers=(),
        _floats=(),
        _datetimes=(),
        _strings=(),
        _booleans=(),
        _exists_together=(),
        _required=(),
        _passthrough=(),
        **param_validators
    ):
        exists_together = []
        for kwarg_group in _exists_together:
            clean_group = []
            for kw in kwarg_group:
                if kw in clean_group:
                    raise ValueError('Keyword argument {!r} repeated in '
                                     'group. Full Group: {!r}'
                                     .format(kw, kwarg_group))
                elif str(kw) != kw:
                    raise ValueError('Keyword argument {!r} should be a '
                                     'string'
                                     .format(kw))
                else:
                    clean_group.append(kw)
            if len(clean_group) == 0:
                raise ValueError('Empty group of arguments makes no sense')
            if len(clean_group) == 1:
                raise ValueError('Group with 1 argument({!r}) makes no sense'
                                 .format(clean_group))
            exists_together.append(tuple(clean_group))
        self.required = tuple(_required)
        self.exists_together_checks = tuple(exists_together)
        self.param_validators = param_validators
        self.param_validators.update(
            **{key: validate_int for key in _integers},
            **{key: validate_float for key in _floats},
            **{key: validate_datetime for key in _datetimes},
            **{key: validate_str for key in _strings},
            **{key: validate_bool for key in _booleans},
            **{key: lambda arg: arg for key in _passthrough}
        )

    def __call__(self, **kwargs):
        for req_kwarg in self.required:
            if req_kwarg not in kwargs:
                raise ValueError('Required keyword argument {!r} was not given'
                                 .format(req_kwarg))
        for kwarg_group in self.exists_together_checks:
            existing = tuple(kw for kw in kwarg_group if kw in kwargs)
            missing = tuple(kw for kw in kwarg_group if kw not in kwargs)
            if len(existing) != 0 and len(missing) != 0:
                # Not a complete group set.
                raise ValueError('Incomplete group. '
                                 'Expecting {!r}. Found {!r}.'
                                 .format(kwarg_group, existing))
        cleaned_kwargs = {}
        for key, value in kwargs.items():
            if key not in self.param_validators:
                raise ValueError('Unknown parameter {!r}.'.format(key))
            validator = self.param_validators[key]
            try:
                cleaned_val = validator(value)
            except ValidationErrors as e:
                raise ValueError('Parameter {!r} failed validation with '
                                 'message {!r}'
                                 .format(key, str(e)))
            cleaned_kwargs[key] = cleaned_val
        return cleaned_kwargs
