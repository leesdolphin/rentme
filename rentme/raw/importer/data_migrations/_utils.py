from django.core.exceptions import ObjectDoesNotExist


def migrate_model(old_model, new_model_cls, **extras):
    if old_model is None:
        return None
    return migrate_merge_model([old_model], new_model_cls, **extras)


def migrate_merge_model(old_models, new_model_cls, **extras):
    if not old_models or all(m is None for m in old_models):
        return None
    lookup_names = model_uniqueness(new_model_cls)
    new_field_names = model_single_field_names(new_model_cls)
    data = {}
    for old_model in old_models:
        if old_model is not None:
            data.update(model_to_dict(old_model, only=new_field_names))
    data.update(extras)
    kwargs = {
        name + '__exact': data[name] for name in lookup_names if name in data
    }
    kwargs['defaults'] = data
    new_model, _ = new_model_cls.objects.update_or_create(**kwargs)
    new_model.save()
    return new_model
    

def model_to_dict(model, only=None, exclude=None):
    if not model:
        return {}
    model_dict = {}
    for key in model_single_field_names(model):
        if only and key not in only:
            continue
        if exclude and key in exclude:
            continue
        try:
            model_dict[key] = getattr(model, key)
        except ObjectDoesNotExist:
            model_dict[key] = None
    return model_dict


def model_uniqueness(model_or_cls):
    if hasattr(model_or_cls, 'Meta') and model_or_cls.Meta.unique_together:
        return frozenset(model_or_cls.Meta.unique_together[0])
    else:
        return frozenset([
            f.name
            for f in model_or_cls._meta.get_fields()
            if not f.is_relation and f.primary_key
        ])


def model_single_field_names(model_or_cls):
    return frozenset(
        [
            f.name
            for f in model_or_cls._meta.get_fields()
            if not f.one_to_many and not f.many_to_many and not f.auto_created
        ]
    )
